import datetime
import uuid
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    NamedTuple,
    Literal,
    overload,
)

import pytz
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, select, JSON, func
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.orm import selectinload
from starlette import status

from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.helper_function import get_comparison
from app.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class NamedFilterFields(NamedTuple):
    field: str
    value: Any
    is_not: bool = False
    greater_then_comp: Optional[Literal["gt", "le"]] = None


excludeList = {
    "id",
    "created_on",
    "updated_on",
}


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    @overload
    async def get(  # noqa: E704
        self,
        session: AsyncSession,
        id: Any,
        *,
        raise_404_error: Literal[True],
        select_in_load: Optional[List[str]] = None,
    ) -> ModelType: ...

    @overload
    async def get(  # noqa: E704
        self,
        session: AsyncSession,
        id: Any,
        *,
        raise_404_error: Literal[False] = False,
        select_in_load: Optional[List[str]] = None,
    ) -> Optional[ModelType]: ...

    async def get(
        self,
        session: AsyncSession,
        id: Any,
        *,
        raise_404_error: bool = False,
        select_in_load: Optional[List[str]] = None,
    ) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id.__eq__(id))
        if select_in_load:
            for attr in select_in_load:
                query = query.options(selectinload(getattr(self.model, attr)))

        result = await session.execute(query)
        first = result.scalars().first()
        if not first and raise_404_error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found",
            )
        return first

    # write a function that iterates over all elements in self.model and return n elements as yield

    async def get_multi(
        self,
        session: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        ids: List[str] = None,
        select_in_load: Optional[List[str]] = None,
    ) -> List[ModelType]:
        query = select(self.model).slice(skip, limit)
        if ids:
            query = query.where(self.model.id.in_(ids))

        if select_in_load:
            for attr in select_in_load:
                query = query.options(selectinload(getattr(self.model, attr)))

        result = await session.execute(query)
        return result.scalars().all()

    async def remove_multi(self, session: AsyncSession, *, ids: List[int]) -> None:
        await session.execute(delete(self.model).where(self.model.id.in_(ids)))
        await session.commit()
        return True

    async def create(
        self, session: AsyncSession, *, obj_in: CreateSchemaType
    ) -> ModelType:
        # get all fields from obj_in that have type datetime
        datetime_fields = [
            (property, value)
            for property, value in vars(obj_in).items()
            if type(value) is datetime.datetime
        ]

        obj_in_data = jsonable_encoder(obj_in)
        for property, value in datetime_fields:
            obj_in_data[property] = value

        db_obj = self.model(**obj_in_data)  # type: ignore
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        skip_refresh: bool = False,
    ) -> ModelType:
        exclude = {
            key
            for key in db_obj.__class__.__annotations__.keys()
            if "ForwardRef" in str(db_obj.__class__.__annotations__[key])
        } | excludeList
        obj_data = jsonable_encoder(
            db_obj,
            exclude=exclude,
        )
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

                if isinstance(db_obj.__table__.columns[field].type, JSON):
                    flag_modified(db_obj, field)

        session.add(db_obj)
        await session.commit()
        if not skip_refresh:
            await session.refresh(db_obj)
        else:
            # manually set the updated_on field
            db_obj.updated_on = datetime.datetime.now(pytz.utc)
        return db_obj

    async def remove(self, session: AsyncSession, *, id: int) -> ModelType:
        obj = await session.get(self.model, id)
        await session.delete(obj)
        await session.commit()
        return obj

    async def iterate(
        self,
        session: AsyncSession,
        *,
        n: int = 100,
        continues: bool = True,
        filter_by: Optional[List[NamedFilterFields]] = None,
    ) -> List[ModelType]:
        """
        Yields `n` elements at a time from the table associated with `self.model`.

        **Parameters**

        * `session`: The SQLAlchemy session object
        * `n`: The number of elements to yield at a time
        continue: If False, the function will continue to yield elements until there are no more elements in the table
        """
        offset = 0
        while True:
            query = select(self.model).offset(offset).limit(n)

            if filter_by:
                for attr, value, is_not, greater_then_comp in filter_by:
                    comparison = get_comparison(
                        getattr(self.model, attr),
                        value,
                        is_not=is_not,
                        greater_then_comp=greater_then_comp,
                    )
                    query = query.where(comparison)

            result = await session.execute(query)
            items = result.scalars().all()
            if not items:
                break
            for item in items:
                yield item
            if continues:
                offset += n

    async def get_count(
        self,
        session: AsyncSession,
        filter_by: Optional[List[NamedFilterFields]] = None,
    ) -> int:
        """
        Returns the total number of elements in the table associated with `self.model`.

        **Parameters**

        * `session`: The SQLAlchemy session object
        """
        query = select(func.count()).select_from(self.model)
        if filter_by:
            for attr, value, is_not, greater_then_comp in filter_by:
                comparison = get_comparison(
                    getattr(self.model, attr),
                    value,
                    is_not=is_not,
                    greater_then_comp=greater_then_comp,
                )
                query = query.where(comparison)

        result = await session.execute(query)
        return result.scalar()
