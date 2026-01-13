"""Pydantic schemas for API validation."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Base schemas
class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(from_attributes=True)


# User schemas
class UserBase(BaseSchema):
    """Base user schema."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: str | None = Field(None, max_length=255)


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseSchema):
    """Schema for updating a user."""

    email: EmailStr | None = None
    username: str | None = Field(None, min_length=3, max_length=100)
    full_name: str | None = Field(None, max_length=255)
    password: str | None = Field(None, min_length=8, max_length=100)
    is_active: bool | None = None


class UserInDB(UserBase):
    """User schema with database fields."""

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class User(UserInDB):
    """Public user schema."""

    pass


# Item schemas
class ItemBase(BaseSchema):
    """Base item schema."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class ItemCreate(ItemBase):
    """Schema for creating an item."""

    pass


class ItemUpdate(BaseSchema):
    """Schema for updating an item."""

    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    is_active: bool | None = None


class ItemInDB(ItemBase):
    """Item schema with database fields."""

    id: int
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class Item(ItemInDB):
    """Public item schema."""

    pass


# Auth schemas
class Token(BaseSchema):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseSchema):
    """Token payload schema."""

    sub: int | None = None
    exp: int | None = None


# Response schemas
class MessageResponse(BaseSchema):
    """Generic message response."""

    message: str


class HealthCheck(BaseSchema):
    """Health check response."""

    status: str
    version: str
    timestamp: datetime
