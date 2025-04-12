from fastapi import APIRouter, HTTPException

from app.dependencies import db_dep, current_user_dep
from app.models import Question
from app.schemas import QuestionResponse, QuestionCreate


router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=list[QuestionResponse])
async def get_questions(db: db_dep):
    return db.query(Question).all()


@router.get("/{id}", response_model=QuestionResponse)
async def get_question(id: int, db: db_dep):
    question = db.query(Question).filter(Question.id == id).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found."
        )
    
    return question


@router.post("/create/", response_model=QuestionResponse)
async def create_question(
        question: QuestionCreate, 
        db: db_dep,
        current_user: current_user_dep
    ):
    db_question = Question(
        **question.model_dump(),
        owner_id=current_user.id
        )

    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    return db_question