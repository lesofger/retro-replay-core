import httpx
import asyncio
from typing import List, Optional, Dict, Any
from config import settings
from models.game_models import MobyGamesGame

class MobyGamesService:
    def __init__(self):
        self.api_key = settings.MOBYGAMES_API_KEY
        self.base_url = "https://api.mobygames.com/v1"

    async def search_games(self, query: str, limit: int = 20) -> List[MobyGamesGame]:
        """Search for games by name"""
        async with httpx.AsyncClient() as client:
            try:
                # Truncate query to 128 characters as per API limits
                search_query = query[:128] if len(query) > 128 else query
                
                # Add small delay to avoid rate limiting
                await asyncio.sleep(0.1)
                
                # Try basic search first without limit parameter
                response = await client.get(
                    f"{self.base_url}/games",
                    params={
                        "api_key": self.api_key,
                        "format": "normal",  # Use 'normal' instead of 'json'
                        "title": search_query
                    }
                )
                
                response.raise_for_status()
                data = response.json()
                
                games = []
                # MobyGames returns data as a dictionary with 'games' key
                game_list = data.get("games", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
                
                # Apply limit manually
                for game_data in game_list[:limit]:
                    try:
                        game = MobyGamesGame(
                            game_id=game_data.get("game_id"),
                            title=game_data.get("title", ""),
                            description=game_data.get("description"),
                            release_date=game_data.get("original_release_date"),
                            platforms=self._extract_platforms(game_data.get("platforms", [])),
                            genres=self._extract_genres(game_data.get("genres", [])),
                            developers=self._extract_developers(game_data.get("developers", [])),
                            publishers=self._extract_publishers(game_data.get("publishers", [])),
                            cover_image_url=game_data.get("sample_cover", {}).get("image"),
                            rating=game_data.get("moby_score")
                        )
                        games.append(game)
                    except Exception as game_error:
                        print(f"Error parsing game data: {game_error}")
                        continue
                
                return games
            except Exception as e:
                print(f"Error searching MobyGames: {e}")
                if 'response' in locals():
                    print(f"Response status: {response.status_code}")
                    print(f"Response text: {response.text}")
                return []

    async def get_game_by_id(self, game_id: int) -> Optional[MobyGamesGame]:
        """Get game details by ID"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/games/{game_id}",
                    params={
                        "api_key": self.api_key,
                        "format": "normal"  # Use 'normal' instead of 'json'
                    }
                )
                response.raise_for_status()
                game_data = response.json()
                
                return MobyGamesGame(
                    game_id=game_data.get("game_id"),
                    title=game_data.get("title", ""),
                    description=game_data.get("description"),
                    release_date=game_data.get("original_release_date"),
                    platforms=self._extract_platforms(game_data.get("platforms", [])),
                    genres=self._extract_genres(game_data.get("genres", [])),
                    developers=self._extract_developers(game_data.get("developers", [])),
                    publishers=self._extract_publishers(game_data.get("publishers", [])),
                    cover_image_url=game_data.get("sample_cover", {}).get("image"),
                    rating=game_data.get("moby_score")
                )
            except Exception as e:
                print(f"Error getting MobyGames game by ID: {e}")
                return None

    def _extract_platforms(self, platforms_data: List[Dict[str, Any]]) -> List[str]:
        """Extract platform names from MobyGames data"""
        return [platform.get("platform_name", "") for platform in platforms_data if platform.get("platform_name")]

    def _extract_genres(self, genres_data: List[Dict[str, Any]]) -> List[str]:
        """Extract genre names from MobyGames data"""
        return [genre.get("genre_name", "") for genre in genres_data if genre.get("genre_name")]

    def _extract_developers(self, developers_data: List[Dict[str, Any]]) -> List[str]:
        """Extract developer names from MobyGames data"""
        return [dev.get("company_name", "") for dev in developers_data if dev.get("company_name")]

    def _extract_publishers(self, publishers_data: List[Dict[str, Any]]) -> List[str]:
        """Extract publisher names from MobyGames data"""
        return [pub.get("company_name", "") for pub in publishers_data if pub.get("company_name")]

    def convert_to_game_model(self, mobygames_game: MobyGamesGame) -> Dict[str, Any]:
        """Convert MobyGames game to our game model format"""
        from datetime import datetime
        
        # Convert release date from string to datetime
        release_date = None
        if mobygames_game.release_date:
            try:
                release_date = datetime.strptime(mobygames_game.release_date, "%Y-%m-%d")
            except ValueError:
                pass  # Keep as None if parsing fails
        
        return {
            "title": mobygames_game.title,
            "description": mobygames_game.description,
            "release_date": release_date,
            "platforms": mobygames_game.platforms or [],
            "genres": mobygames_game.genres or [],
            "developers": mobygames_game.developers or [],
            "publishers": mobygames_game.publishers or [],
            "cover_image_url": mobygames_game.cover_image_url,
            "rating": mobygames_game.rating,
            "mobygames_id": mobygames_game.game_id
        }
