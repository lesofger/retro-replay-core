from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from services.igdb_service import IGDBService
from services.mobygames_service import MobyGamesService

router = APIRouter(prefix="/games", tags=["games"])

# Initialize services
igdb_service = IGDBService()
mobygames_service = MobyGamesService()

@router.get("/")
async def get_games():
    """Get information about available game search endpoints"""
    return {
        "message": "Game search endpoints available",
        "endpoints": {
            "search_igdb": "/games/search/igdb",
            "search_mobygames": "/games/search/mobygames",
            "platforms": "/games/platforms",
            "genres": "/games/genres",
            "game_modes": "/games/game-modes",
            "collections": "/games/collections",
            "franchises": "/games/franchises"
        },
        "note": "Use WooCommerce endpoints for product management"
    }

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

@router.get("/igdb/{igdb_id}")
async def get_igdb_game(igdb_id: int):
    """Get a specific game from IGDB by ID"""
    try:
        game = await igdb_service.get_game_by_id(igdb_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found on IGDB")
        return game
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/mobygames/{mobygames_id}")
async def get_mobygames_game(mobygames_id: int):
    """Get a specific game from MobyGames by ID"""
    try:
        game = await mobygames_service.get_game_by_id(mobygames_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found on MobyGames")
        return game
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
