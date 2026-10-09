from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(tags=["me"])


@router.get("/me", response_model=UserRead)
async def read_me(user: Annotated[User, Depends(get_current_user)]) -> User:
    return user
