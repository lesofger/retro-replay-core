import httpx
import asyncio
from typing import List, Optional, Dict, Any
from config import settings
from models.game_models import IGDBGame

class IGDBService:
    def __init__(self):
        self.client_id = settings.IGDB_CLIENT_ID
        self.client_secret = settings.IGDB_CLIENT_SECRET
        self.base_url = "https://api.igdb.com/v4"
        self.access_token = None
        self.token_expires_at = None

    async def _get_access_token(self) -> str:
        """Get access token for IGDB API"""
        if self.access_token and self.token_expires_at and self.token_expires_at > asyncio.get_event_loop().time():
            return self.access_token

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://id.twitch.tv/oauth2/token",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "client_credentials"
                }
            )
            response.raise_for_status()
            token_data = response.json()
            
            self.access_token = token_data["access_token"]
            self.token_expires_at = asyncio.get_event_loop().time() + token_data["expires_in"]
            
            return self.access_token

    async def _make_request(self, endpoint: str, query: str) -> List[Dict[str, Any]]:
        """Make authenticated request to IGDB API"""
        token = await self._get_access_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/{endpoint}",
                headers={
                    "Client-ID": self.client_id,
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "text/plain"
                },
                content=query
            )
            response.raise_for_status()
            return response.json()

    async def search_games(self, query: str, limit: int = 20, offset: int = 0, platform_id: Optional[int] = None) -> List[IGDBGame]:
        """Search for games by name with optional platform filtering and pagination"""
        # Build the search query
        search_parts = [f'search "{query}"']
        
        # Add platform filter if specified
        if platform_id:
            search_parts.append(f'where platforms = {platform_id}')
        
        # Add fields and pagination
        search_parts.append('fields id,name,summary,first_release_date,platforms,genres,involved_companies,cover,rating,rating_count')
        search_parts.append(f'limit {limit}')
        search_parts.append(f'offset {offset}')
        
        search_query = '; '.join(search_parts) + ';'

        try:
            results = await self._make_request("games", search_query)
            return [IGDBGame(**game) for game in results]
        except Exception as e:
            print(f"Error searching games: {e}")
            return []

    async def get_game_by_id(self, game_id: int) -> Optional[IGDBGame]:
        """Get game details by ID"""
        query = f'fields id,name,summary,first_release_date,platforms,genres,involved_companies,cover,rating,rating_count; where id = {game_id};'
        
        try:
            results = await self._make_request("games", query)
            if results:
                return IGDBGame(**results[0])
            return None
        except Exception as e:
            print(f"Error getting game by ID: {e}")
            return None

    async def get_platforms(self) -> List[Dict[str, Any]]:
        """Get list of platforms"""
        query = "fields id,name,abbreviation; limit 500;"
        
        try:
            return await self._make_request("platforms", query)
        except Exception as e:
            print(f"Error getting platforms: {e}")
            return []

    async def get_genres(self) -> List[Dict[str, Any]]:
        """Get list of genres"""
        query = "fields id,name; limit 500;"
        
        try:
            return await self._make_request("genres", query)
        except Exception as e:
            print(f"Error getting genres: {e}")
            return []

    async def convert_to_game_model(self, igdb_game: IGDBGame) -> Dict[str, Any]:
        """Convert IGDB game to our game model format"""
        from datetime import datetime
        
        # Convert release date from timestamp to datetime
        release_date = None
        if igdb_game.first_release_date:
            release_date = datetime.fromtimestamp(igdb_game.first_release_date)
        
        # Extract platform names
        platforms = []
        if igdb_game.platforms:
            try:
                platform_query = f"fields id,name; where id = ({','.join(map(str, igdb_game.platforms))});"
                platform_results = await self._make_request("platforms", platform_query)
                platforms = [platform.get("name", "Unknown") for platform in platform_results]
            except Exception as e:
                print(f"Error fetching platform details: {e}")
                platforms = ["Unknown"] * len(igdb_game.platforms)
        
        # Extract genre names
        genres = []
        if igdb_game.genres:
            try:
                genre_query = f"fields id,name; where id = ({','.join(map(str, igdb_game.genres))});"
                genre_results = await self._make_request("genres", genre_query)
                genres = [genre.get("name", "Unknown") for genre in genre_results]
            except Exception as e:
                print(f"Error fetching genre details: {e}")
                genres = ["Unknown"] * len(igdb_game.genres)
        
        # Extract company names
        developers = []
        publishers = []
        if igdb_game.involved_companies:
            try:
                company_query = f"fields id,name,developer,publisher; where id = ({','.join(map(str, igdb_game.involved_companies))});"
                company_results = await self._make_request("involved_companies", company_query)
                
                for company in company_results:
                    company_name = company.get("name", "Unknown")
                    if company.get("developer", False):
                        developers.append(company_name)
                    if company.get("publisher", False):
                        publishers.append(company_name)
            except Exception as e:
                print(f"Error fetching company details: {e}")
                developers = ["Unknown"]
                publishers = ["Unknown"]
        
        # Get cover image URL
        cover_image_url = None
        if igdb_game.cover:
            cover_image_url = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{igdb_game.cover}.jpg"
        
        return {
            "title": igdb_game.name,
            "description": igdb_game.summary,
            "release_date": release_date,
            "platforms": platforms,
            "genres": genres,
            "developers": developers,
            "publishers": publishers,
            "cover_image_url": cover_image_url,
            "rating": igdb_game.rating,
            "igdb_id": igdb_game.id
        }
