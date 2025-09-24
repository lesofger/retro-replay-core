from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class Platform(str, Enum):
    PC = "PC"
    PLAYSTATION = "PlayStation"
    XBOX = "Xbox"
    NINTENDO = "Nintendo"
    MOBILE = "Mobile"
    OTHER = "Other"

class GameStatus(str, Enum):
    WANT_TO_PLAY = "want_to_play"
    PLAYING = "playing"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"

class GameBase(BaseModel):
    title: str
    description: Optional[str] = None
    release_date: Optional[datetime] = None
    platforms: List[Platform] = []
    genres: List[str] = []
    developers: List[str] = []
    publishers: List[str] = []
    cover_image_url: Optional[str] = None
    rating: Optional[float] = None
    status: GameStatus = GameStatus.WANT_TO_PLAY
    notes: Optional[str] = None

class GameCreate(GameBase):
    igdb_id: Optional[int] = None
    mobygames_id: Optional[int] = None

class GameUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    release_date: Optional[datetime] = None
    platforms: Optional[List[Platform]] = None
    genres: Optional[List[str]] = None
    developers: Optional[List[str]] = None
    publishers: Optional[List[str]] = None
    cover_image_url: Optional[str] = None
    rating: Optional[float] = None
    status: Optional[GameStatus] = None
    notes: Optional[str] = None

class Game(GameBase):
    id: int
    igdb_id: Optional[int] = None
    mobygames_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class IGDBGame(BaseModel):
    id: int
    name: str
    summary: Optional[str] = None
    first_release_date: Optional[int] = None
    platforms: Optional[List[int]] = None  # IGDB returns platform IDs as integers
    genres: Optional[List[int]] = None     # IGDB returns genre IDs as integers
    involved_companies: Optional[List[int]] = None  # IGDB returns company IDs as integers
    cover: Optional[int] = None            # IGDB returns cover ID as integer
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    # New fields
    game_modes: Optional[List[int]] = None  # Game mode IDs
    collection: Optional[int] = None        # Series/Collection ID
    franchise: Optional[int] = None         # Franchise ID
    storyline: Optional[str] = None         # Story description
    alternative_names: Optional[List[int]] = None  # Alternative title IDs
    age_ratings: Optional[List[int]] = None # Age rating IDs
    websites: Optional[List[int]] = None    # Website/link IDs
    release_dates: Optional[List[int]] = None  # Release date IDs
    screenshots: Optional[List[Dict[str, Any]]] = None # Screenshot objects with id and url
    artworks: Optional[List[int]] = None    # Artwork IDs
    videos: Optional[List[int]] = None      # Video IDs

class MobyGamesGame(BaseModel):
    game_id: int
    title: str
    description: Optional[str] = None
    release_date: Optional[str] = None
    platforms: Optional[List[str]] = None
    genres: Optional[List[str]] = None
    developers: Optional[List[str]] = None
    publishers: Optional[List[str]] = None
    cover_image_url: Optional[str] = None
    rating: Optional[float] = None
