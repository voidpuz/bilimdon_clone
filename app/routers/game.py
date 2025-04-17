from fastapi import APIRouter, HTTPException

from datetime import timezone, datetime, timedelta

from app.dependencies import db_dep, current_user_dep, admin_user_dep
from app.models import Game
from app.schemas import GameCreate, GameResponse, GameUpdate


router = APIRouter(prefix="/games", tags=["games"])


@router.get("/", response_model=list[GameResponse])
async def get_games(db: db_dep):
    return db.query(Game).filter(
        Game.end_time > datetime.now(timezone.utc)
    )


@router.get("/all/", response_model=list[GameResponse])
async def get_games(db: db_dep):
    return db.query(Game).all()


@router.get("/{id}/", response_model=GameResponse)
async def get_game(id: int, db: db_dep):
    game = db.query(Game).filter(Game.id == id).first()

    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found."
        )
    
    return game


@router.post("/create/", response_model=GameResponse)
async def create_game(
        game: GameCreate, 
        db: db_dep,
        current_user: current_user_dep
    ):
    if game.start_time > game.end_time:
        raise HTTPException(
            status_code=400,
            detail="Start time must be before end time."
        )

    if game.start_time < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Start time must be in the future."
        )
    
    if game.end_time - game.start_time < timedelta(hours=1):
        raise HTTPException(
            status_code=400,
            detail="Game must last at least 1 hour."
        )

    db_game = Game(
        **game.model_dump(),
        owner_id=current_user.id
    )

    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game


@router.patch("/update/{id}", response_model=GameResponse)
async def update_game(
        id: int, 
        game: GameUpdate, 
        db: db_dep
    ):
    db_game = db.query(Game).filter(Game.id == id).first()

    if not db_game:
        raise HTTPException(
            status_code=404,
            detail="Game not found."
        )

    # if game.start_time and not game.start_time.tzinfo:
    #     game.start_time = game.start_time.replace(tzinfo=timezone.utc)
    
    # is_permissible = db_game.start_time < datetime.now(timezone.utc)
    # if is_permissible:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="You cannot update this game, as it already started or finished."
    #     )

    db_game.title = game.title if game.title else db_game.title
    db_game.description = game.description if game.description else db_game.description
    db_game.end_time = game.end_time if game.end_time else db_game.end_time
    db_game.topic_id = game.topic_id if game.topic_id else db_game.topic_id

    db.commit()
    db.refresh(db_game)

    return db_game


@router.delete("/delete/{id}")
async def delete_game(
        id: int, 
        db: db_dep,
        admin_user: admin_user_dep
    ):
    db_game = db.query(Game).filter(Game.id == id).first()

    if not db_game:
        raise HTTPException(
            status_code=404,
            detail="Game not found."
        )

    db.delete(db_game)
    db.commit()

    return {
        "game_id": id,
        "message": "Game deleted."
    }