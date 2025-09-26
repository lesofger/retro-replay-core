from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class IGDBGame(BaseModel):
    id: int
    name: str
    summary: Optional[str] = None
    first_release_date: Optional[int] = None
    platforms: Optional[List[Dict[str, Any]]] = None
    genres: Optional[List[Dict[str, Any]]] = None
    involved_companies: Optional[List[Dict[str, Any]]] = None
    cover: Optional[Dict[str, Any]] = None
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    game_modes: Optional[List[int]] = None
    collection: Optional[int] = None
    franchise: Optional[int] = None
    storyline: Optional[str] = None
    alternative_names: Optional[List[int]] = None
    age_ratings: Optional[List[int]] = None
    websites: Optional[List[int]] = None
    release_dates: Optional[List[int]] = None
    screenshots: Optional[List[Dict[str, Any]]] = None
    artworks: Optional[List[int]] = None
    videos: Optional[List[int]] = None

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
