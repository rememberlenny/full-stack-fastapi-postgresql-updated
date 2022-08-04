import pytest
from fastapi.encoders import jsonable_encoder
#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.security import verify_password
from app.users.schemas import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string


pytestmark = pytest.mark.asyncio

async def test_create_user(async_get_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud.user.create(async_get_db, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


async def test_authenticate_user(async_get_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud.user.create(async_get_db, obj_in=user_in)
    authenticated_user = await crud.user.authenticate(async_get_db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


async def test_not_authenticate_user(async_get_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user = await crud.user.authenticate(async_get_db, email=email, password=password)
    assert user is None


async def test_check_if_user_is_inactive(async_get_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud.user.create(async_get_db, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active is False


async def test_check_if_user_is_active_inactive(async_get_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_active=True)
    user = await crud.user.create(async_get_db, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active


async def test_check_if_user_is_superuser(async_get_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = await crud.user.create(async_get_db, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is True

async def test_check_if_user_is_superuser_normal_user(async_get_db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud.user.create(async_get_db, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is False

async def test_get_user(async_get_db: AsyncSession) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = await crud.user.create(async_get_db, obj_in=user_in)
    user_2 = await crud.user.get(async_get_db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)

async def test_update_user(async_get_db: AsyncSession) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = await crud.user.create(async_get_db, obj_in=user_in)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    await crud.user.update(async_get_db, db_obj=user, obj_in=user_in_update)
    user_2 = await crud.user.get(async_get_db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
