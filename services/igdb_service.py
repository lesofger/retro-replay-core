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
        search_parts.append('fields id,name,summary,first_release_date,platforms,genres,involved_companies,cover,rating,rating_count,game_modes,collection,franchise,storyline,alternative_names,age_ratings,websites,release_dates,screenshots,artworks,videos')
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
        query = f'fields id,name,summary,first_release_date,platforms,genres,involved_companies,cover,rating,rating_count,game_modes,collection,franchise,storyline,alternative_names,age_ratings,websites,release_dates,screenshots,artworks,videos; where id = {game_id};'
        
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

    async def get_game_modes(self) -> List[Dict[str, Any]]:
        """Get list of game modes"""
        query = "fields id,name; limit 500;"
        
        try:
            return await self._make_request("game_modes", query)
        except Exception as e:
            print(f"Error getting game modes: {e}")
            return []

    async def get_collections(self) -> List[Dict[str, Any]]:
        """Get list of collections/series"""
        query = "fields id,name; limit 500;"
        
        try:
            return await self._make_request("collections", query)
        except Exception as e:
            print(f"Error getting collections: {e}")
            return []

    async def get_franchises(self) -> List[Dict[str, Any]]:
        """Get list of franchises"""
        query = "fields id,name; limit 500;"
        
        try:
            return await self._make_request("franchises", query)
        except Exception as e:
            print(f"Error getting franchises: {e}")
            return []

    async def get_age_ratings(self) -> List[Dict[str, Any]]:
        """Get list of age ratings"""
        query = "fields id,category,rating; limit 500;"
        
        try:
            return await self._make_request("age_ratings", query)
        except Exception as e:
            print(f"Error getting age ratings: {e}")
            return []

    async def get_websites(self) -> List[Dict[str, Any]]:
        """Get list of websites"""
        query = "fields id,category,url; limit 500;"
        
        try:
            return await self._make_request("websites", query)
        except Exception as e:
            print(f"Error getting websites: {e}")
            return []

    async def get_release_dates(self) -> List[Dict[str, Any]]:
        """Get list of release dates"""
        query = "fields id,date,platform,region; limit 500;"
        
        try:
            return await self._make_request("release_dates", query)
        except Exception as e:
            print(f"Error getting release dates: {e}")
            return []

    async def get_screenshots(self) -> List[Dict[str, Any]]:
        """Get list of screenshots"""
        query = "fields id,url; limit 500;"
        
        try:
            return await self._make_request("screenshots", query)
        except Exception as e:
            print(f"Error getting screenshots: {e}")
            return []

    async def get_artworks(self) -> List[Dict[str, Any]]:
        """Get list of artworks"""
        query = "fields id,url; limit 500;"
        
        try:
            return await self._make_request("artworks", query)
        except Exception as e:
            print(f"Error getting artworks: {e}")
            return []

    async def get_videos(self) -> List[Dict[str, Any]]:
        """Get list of videos"""
        query = "fields id,name,video_id; limit 500;"
        
        try:
            return await self._make_request("game_videos", query)
        except Exception as e:
            print(f"Error getting videos: {e}")
            return []

    async def get_alternative_names(self) -> List[Dict[str, Any]]:
        """Get list of alternative names"""
        query = "fields id,name; limit 500;"
        
        try:
            return await self._make_request("alternative_names", query)
        except Exception as e:
            print(f"Error getting alternative names: {e}")
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
        
        # Extract game modes
        game_modes = []
        if igdb_game.game_modes:
            try:
                game_mode_query = f"fields id,name; where id = ({','.join(map(str, igdb_game.game_modes))});"
                game_mode_results = await self._make_request("game_modes", game_mode_query)
                game_modes = [mode.get("name", "Unknown") for mode in game_mode_results]
            except Exception as e:
                print(f"Error fetching game mode details: {e}")
                game_modes = ["Unknown"] * len(igdb_game.game_modes)
        
        # Extract series/collection
        series = None
        if igdb_game.collection:
            try:
                collection_query = f"fields id,name; where id = {igdb_game.collection};"
                collection_results = await self._make_request("collections", collection_query)
                if collection_results:
                    series = collection_results[0].get("name", "Unknown")
            except Exception as e:
                print(f"Error fetching collection details: {e}")
                series = "Unknown"
        
        # Extract franchise
        franchise = None
        if igdb_game.franchise:
            try:
                franchise_query = f"fields id,name; where id = {igdb_game.franchise};"
                franchise_results = await self._make_request("franchises", franchise_query)
                if franchise_results:
                    franchise = franchise_results[0].get("name", "Unknown")
            except Exception as e:
                print(f"Error fetching franchise details: {e}")
                franchise = "Unknown"
        
        # Extract alternative names
        alternative_titles = []
        if igdb_game.alternative_names:
            try:
                alt_name_query = f"fields id,name; where id = ({','.join(map(str, igdb_game.alternative_names))});"
                alt_name_results = await self._make_request("alternative_names", alt_name_query)
                alternative_titles = [alt.get("name", "Unknown") for alt in alt_name_results]
            except Exception as e:
                print(f"Error fetching alternative name details: {e}")
                alternative_titles = ["Unknown"] * len(igdb_game.alternative_names)
        
        # Extract age ratings
        age_ratings = []
        if igdb_game.age_ratings:
            try:
                age_rating_query = f"fields id,category,rating; where id = ({','.join(map(str, igdb_game.age_ratings))});"
                age_rating_results = await self._make_request("age_ratings", age_rating_query)
                age_ratings = [f"{rating.get('rating', 'Unknown')} ({rating.get('category', 'Unknown')})" for rating in age_rating_results]
            except Exception as e:
                print(f"Error fetching age rating details: {e}")
                age_ratings = ["Unknown"] * len(igdb_game.age_ratings)
        
        # Extract websites/links
        links = []
        if igdb_game.websites:
            try:
                website_query = f"fields id,category,url; where id = ({','.join(map(str, igdb_game.websites))});"
                website_results = await self._make_request("websites", website_query)
                links = [{"category": site.get("category", "Unknown"), "url": site.get("url", "")} for site in website_results]
            except Exception as e:
                print(f"Error fetching website details: {e}")
                links = [{"category": "Unknown", "url": ""}] * len(igdb_game.websites)
        
        # Extract release dates
        releases = []
        if igdb_game.release_dates:
            try:
                release_query = f"fields id,date,platform,region; where id = ({','.join(map(str, igdb_game.release_dates))});"
                release_results = await self._make_request("release_dates", release_query)
                releases = []
                for release in release_results:
                    release_date_str = None
                    if release.get("date"):
                        release_date_str = datetime.fromtimestamp(release["date"]).strftime("%Y-%m-%d")
                    releases.append({
                        "date": release_date_str,
                        "platform": release.get("platform", "Unknown"),
                        "region": release.get("region", "Unknown")
                    })
            except Exception as e:
                print(f"Error fetching release date details: {e}")
                releases = [{"date": None, "platform": "Unknown", "region": "Unknown"}] * len(igdb_game.release_dates)
        
        # Extract screenshots and artworks (with 8 image limit)
        images = []
        all_image_ids = []
        if igdb_game.screenshots:
            all_image_ids.extend(igdb_game.screenshots)
        if igdb_game.artworks:
            all_image_ids.extend(igdb_game.artworks)
        
        # Limit to 8 images max
        all_image_ids = all_image_ids[:8]
        
        if all_image_ids:
            try:
                # Get screenshots
                if igdb_game.screenshots:
                    screenshot_query = f"fields id,url; where id = ({','.join(map(str, igdb_game.screenshots[:8]))});"
                    screenshot_results = await self._make_request("screenshots", screenshot_query)
                    for screenshot in screenshot_results:
                        if screenshot.get("url"):
                            images.append({
                                "type": "screenshot",
                                "url": f"https://images.igdb.com/igdb/image/upload/t_screenshot_big/{screenshot['url']}.jpg"
                            })
                
                # Get artworks (fill remaining slots up to 8)
                remaining_slots = 8 - len(images)
                if remaining_slots > 0 and igdb_game.artworks:
                    artwork_query = f"fields id,url; where id = ({','.join(map(str, igdb_game.artworks[:remaining_slots]))});"
                    artwork_results = await self._make_request("artworks", artwork_query)
                    for artwork in artwork_results:
                        if artwork.get("url"):
                            images.append({
                                "type": "artwork",
                                "url": f"https://images.igdb.com/igdb/image/upload/t_artwork_big/{artwork['url']}.jpg"
                            })
            except Exception as e:
                print(f"Error fetching image details: {e}")
                images = []
        
        # Extract videos (YouTube URLs)
        videos = []
        if igdb_game.videos:
            try:
                video_query = f"fields id,name,video_id; where id = ({','.join(map(str, igdb_game.videos))});"
                video_results = await self._make_request("game_videos", video_query)
                videos = []
                for video in video_results:
                    if video.get("video_id"):
                        videos.append({
                            "name": video.get("name", "Unknown"),
                            "youtube_url": f"https://www.youtube.com/watch?v={video['video_id']}",
                            "embed_url": f"https://www.youtube.com/embed/{video['video_id']}"
                        })
            except Exception as e:
                print(f"Error fetching video details: {e}")
                videos = []
        
        # Get cover image URL
        cover_image_url = None
        if igdb_game.cover:
            cover_image_url = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{igdb_game.cover}.jpg"
        
        return {
            "title": igdb_game.name,
            "description": igdb_game.summary,
            "storyline": igdb_game.storyline,
            "release_date": release_date,
            "platforms": platforms,
            "genres": genres,
            "developers": developers,
            "publishers": publishers,
            "game_modes": game_modes,
            "series": series,
            "franchise": franchise,
            "alternative_titles": alternative_titles,
            "age_ratings": age_ratings,
            "links": links,
            "releases": releases,
            "images": images,  # Screenshots and artworks combined, max 8
            "videos": videos,  # YouTube URLs
            "cover_image_url": cover_image_url,
            "rating": igdb_game.rating,
            "igdb_id": igdb_game.id
        }
