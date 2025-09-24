from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database.database import get_db
from database.models import Game
from models.game_models import GameCreate, GameUpdate, Game as GameModel
from services.igdb_service import IGDBService
from services.mobygames_service import MobyGamesService

router = APIRouter(prefix="/games", tags=["games"])

# Initialize services
igdb_service = IGDBService()
mobygames_service = MobyGamesService()

@router.get("/", response_model=List[GameModel])
async def get_games(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all games in the library with optional filtering"""
    query = db.query(Game)
    
    if search:
        query = query.filter(Game.title.contains(search))
    
    if status:
        query = query.filter(Game.status == status)
    
    games = query.offset(skip).limit(limit).all()
    return games

@router.get("/{game_id}", response_model=GameModel)
async def get_game(game_id: int, db: Session = Depends(get_db)):
    """Get a specific game by ID"""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.post("/", response_model=GameModel)
async def create_game(game: GameCreate, db: Session = Depends(get_db)):
    """Add a new game to the library"""
    db_game = Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.put("/{game_id}", response_model=GameModel)
async def update_game(game_id: int, game_update: GameUpdate, db: Session = Depends(get_db)):
    """Update an existing game"""
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    update_data = game_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_game, field, value)
    
    db.commit()
    db.refresh(db_game)
    return db_game

@router.delete("/{game_id}")
async def delete_game(game_id: int, db: Session = Depends(get_db)):
    """Delete a game from the library"""
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    db.delete(db_game)
    db.commit()
    return {"message": "Game deleted successfully"}

@router.get("/search/igdb")
async def search_igdb_games(
    query: str = Query(..., description="Search query for games"),
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0, description="Number of results to skip for pagination"),
    platform_id: Optional[int] = Query(None, description="Filter by platform ID (use /platforms endpoint to get platform IDs)")
):
    """Search for games on IGDB with optional platform filtering and pagination"""
    games = await igdb_service.search_games(query, limit, offset, platform_id)
    return games

@router.get("/platforms")
async def get_platforms():
    """Get list of available platforms from IGDB"""
    platforms = await igdb_service.get_platforms()
    return platforms

@router.get("/game-modes")
async def get_game_modes():
    """Get list of available game modes from IGDB"""
    game_modes = await igdb_service.get_game_modes()
    return game_modes

@router.get("/genres")
async def get_genres():
    """Get list of available genres from IGDB"""
    genres = await igdb_service.get_genres()
    return genres

@router.get("/collections")
async def get_collections():
    """Get list of available collections/series from IGDB"""
    collections = await igdb_service.get_collections()
    return collections

@router.get("/franchises")
async def get_franchises():
    """Get list of available franchises from IGDB"""
    franchises = await igdb_service.get_franchises()
    return franchises

@router.get("/search/mobygames")
async def search_mobygames_games(
    query: str = Query(..., description="Search query for games"),
    limit: int = Query(20, ge=1, le=50)
):
    """Search for games on MobyGames"""
    games = await mobygames_service.search_games(query, limit)
    return games

@router.post("/import/igdb/{igdb_id}")
async def import_from_igdb(igdb_id: int, db: Session = Depends(get_db)):
    """Import a game from IGDB by ID"""
    # Check if game already exists
    existing_game = db.query(Game).filter(Game.igdb_id == igdb_id).first()
    if existing_game:
        raise HTTPException(status_code=400, detail="Game already exists in library")
    
    # Fetch game from IGDB
    igdb_game = await igdb_service.get_game_by_id(igdb_id)
    if not igdb_game:
        raise HTTPException(status_code=404, detail="Game not found on IGDB")
    
    # Convert to our model format
    game_data = await igdb_service.convert_to_game_model(igdb_game)
    game_data["igdb_id"] = igdb_id
    
    # Create game in database
    db_game = Game(**game_data)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    
    return db_game

@router.post("/import/mobygames/{mobygames_id}")
async def import_from_mobygames(mobygames_id: int, db: Session = Depends(get_db)):
    """Import a game from MobyGames by ID"""
    # Check if game already exists
    existing_game = db.query(Game).filter(Game.mobygames_id == mobygames_id).first()
    if existing_game:
        raise HTTPException(status_code=400, detail="Game already exists in library")
    
    # Fetch game from MobyGames
    mobygames_game = await mobygames_service.get_game_by_id(mobygames_id)
    if not mobygames_game:
        raise HTTPException(status_code=404, detail="Game not found on MobyGames")
    
    # Convert to our model format
    game_data = mobygames_service.convert_to_game_model(mobygames_game)
    game_data["mobygames_id"] = mobygames_id
    
    # Create game in database
    db_game = Game(**game_data)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    
    return db_game

@router.get("/stats/summary")
async def get_library_stats(db: Session = Depends(get_db)):
    """Get library statistics"""
    total_games = db.query(Game).count()
    
    # Count by status
    status_counts = {}
    for status in ["want_to_play", "playing", "completed", "on_hold", "dropped"]:
        count = db.query(Game).filter(Game.status == status).count()
        status_counts[status] = count
    
    # Count by platform
    platform_counts = {}
    games = db.query(Game).all()
    for game in games:
        if game.platforms:
            for platform in game.platforms:
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
    
    return {
        "total_games": total_games,
        "status_breakdown": status_counts,
        "platform_breakdown": platform_counts
    }
