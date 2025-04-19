from fastapi import APIRouter, Depends, HTTPException
from app import models, schemas
from app.dependencies import current_user_dep, admin_user_dep
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=schemas.UserRead)
def get_user_info(current_user: models.User = Depends(current_user_dep)):
    return current_user

