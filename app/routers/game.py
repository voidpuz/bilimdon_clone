from fastapi import APIRouter, HTTPException

from app.dependencies import db_dep, current_user_dep
from app.models import Game


router = APIRouter(prefix="/games", tags=["games"])

