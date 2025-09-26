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

class MobyGamesAlternateTitle(BaseModel):
    description: str
    title: str

class MobyGamesGenre(BaseModel):
    genre_category: str
    genre_category_id: int
    genre_id: int
    genre_name: str

class MobyGamesPlatform(BaseModel):
    first_release_date: Optional[str] = None
    platform_id: int
    platform_name: str

class MobyGamesCover(BaseModel):
    height: int
    image: str
    platforms: List[str]
    thumbnail_image: str
    width: int

class MobyGamesScreenshot(BaseModel):
    caption: str
    height: int
    image: str
    thumbnail_image: str
    width: int

class MobyGamesGame(BaseModel):
    game_id: int
    title: str
    description: Optional[str] = None
    alternate_titles: Optional[List[MobyGamesAlternateTitle]] = None
    genres: Optional[List[MobyGamesGenre]] = None
    platforms: Optional[List[MobyGamesPlatform]] = None
    developers: Optional[List[Dict[str, Any]]] = None
    publishers: Optional[List[Dict[str, Any]]] = None
    sample_cover: Optional[MobyGamesCover] = None
    sample_screenshots: Optional[List[MobyGamesScreenshot]] = None
    moby_score: Optional[float] = None
    num_votes: Optional[int] = None
    moby_url: Optional[str] = None
    official_url: Optional[str] = None
