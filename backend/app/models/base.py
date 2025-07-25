from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import Mapped
from sqlmodel import Field, SQLModel


class Base(SQLModel):
    """Base model for all SQLModel models in the application.

    This class provides common fields and functionality that should be inherited
    by all database models. It includes automatic timestamping and sensible
    defaults for primary keys.

    Attributes:
        id: Primary key field with auto-increment
        created_at: Timestamp when the record was created (auto-set on insert)
        updated_at: Timestamp when the record was last updated (auto-set on insert/update)
    """

    # Primary key with auto-increment
    id: Mapped[int | None] = Field(
        default=None,
        primary_key=True,
        description="Unique identifier for the record",
        index=True,
    )

    # Creation timestamp - set once when record is created
    created_at: Mapped[datetime | None] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        ),
        description="When this record was created",
    )

    # Update timestamp - automatically updated on any change
    updated_at: Mapped[datetime | None] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
        description="When this record was last updated",
    )

    def __repr__(self) -> str:
        """String representation of the model."""
        class_name = self.__class__.__name__
        if self.id:
            return f"<{class_name}(id={self.id})>"
        return f"<{class_name}(new)>"


# Alternative base class with soft delete functionality
class SoftDeleteBase(Base):
    """Base model with soft delete functionality.

    Extends the Base model to include soft delete capability.
    Records are marked as deleted rather than physically removed.
    """

    deleted_at: Mapped[datetime | None] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
        description="When this record was deleted (null if not deleted)",
    )

    is_deleted: Mapped[bool] = Field(
        default=False, description="Whether this record has been soft deleted"
    )

    def soft_delete(self) -> None:
        """Mark this record as deleted."""
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        """Restore a soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None


# Example usage of the enhanced base model
# class User(Base, table=True):
#     """Example user model inheriting from Base."""

#     __tablename__ = "users"

#     email: Mapped[str] = Field(
#         index=True,
#         unique=True,
#         description="User's email address"
#     )
#     name: Mapped[str] = Field(
#         description="User's full name"
#     )
#     is_active: Mapped[bool] = Field(
#         default=True,
#         description="Whether the user account is active"
#     )
