"""User service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.repositories.user_repository import user_repository
from app.schemas import User, UserCreate, UserUpdate


class UserService:
    """Business logic for users."""

    def __init__(self) -> None:
        """Initialize user service."""
        self.repository = user_repository

    async def create_user(
        self,
        db: AsyncSession,
        user_in: UserCreate,
    ) -> User:
        """Create new user with hashed password."""
        # Check if email exists
        existing = await self.repository.get_by_email(db, user_in.email)
        if existing:
            raise ValueError("Email already registered")

        # Check if username exists
        existing = await self.repository.get_by_username(db, user_in.username)
        if existing:
            raise ValueError("Username already taken")

        # Hash password and create user
        user_dict = user_in.model_dump()
        user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))

        user = await self.repository.create(db, UserCreate(**user_dict))
        return User.model_validate(user)

    async def authenticate(
        self,
        db: AsyncSession,
        username: str,
        password: str,
    ) -> User | None:
        """Authenticate user by username and password."""
        user = await self.repository.get_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return User.model_validate(user)

    async def get_user(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> User | None:
        """Get user by ID."""
        user = await self.repository.get(db, user_id)
        if not user:
            return None
        return User.model_validate(user)

    async def update_user(
        self,
        db: AsyncSession,
        user_id: int,
        user_in: UserUpdate,
    ) -> User | None:
        """Update user."""
        user = await self.repository.get(db, user_id)
        if not user:
            return None

        # Hash password if provided
        if user_in.password:
            user_dict = user_in.model_dump(exclude_unset=True)
            user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
            user_in = UserUpdate(**user_dict)

        updated_user = await self.repository.update(db, user, user_in)
        return User.model_validate(updated_user)

    async def delete_user(
        self,
        db: AsyncSession,
        user_id: int,
    ) -> bool:
        """Delete user."""
        return await self.repository.delete(db, user_id)


user_service = UserService()
