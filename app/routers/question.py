from fastapi import APIRouter

from app.dependencies import db_dep
from app.models import Question
from app.schemas import QuestionListResponse


router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=list[QuestionListResponse])
async def get_questions(db: db_dep):
    return db.query(Question).all()


