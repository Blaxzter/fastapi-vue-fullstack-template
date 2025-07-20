# SQLModels

Uses the [SQLModel](https://sqlmodel.tiangolo.com/) library to define the data models for the application.
Based on [Pydantic](https://pydantic-docs.helpmanual.io/) and [SQLAlchemy](https://www.sqlalchemy.org/), it provides a powerful way to define models that can be used for both data validation and database interaction.

## Example Model Structure

```
from sqlmodel import SQLModel, Field


class SongBase(SQLModel):
    name: str
    artist: str


class Song(SongBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class SongCreate(SongBase):
    pass
```
