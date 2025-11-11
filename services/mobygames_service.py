import httpx
import asyncio
import re
from typing import List, Optional, Dict, Any
from config import settings
from models.external_api_models import MobyGamesGame, MobyGamesAlternateTitle, MobyGamesGenre, MobyGamesPlatform, MobyGamesCover, MobyGamesScreenshot

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
                        game = self._parse_game_data(game_data)
                        games.append(game)
                    except Exception as game_error:
                        print(f"Error parsing game data: {game_error}")
                        continue
                
                return games
            except Exception as e:
                print(f"Errors in searching MobyGames: {e}")
                if 'response' in locals():
                    print(f"Responses status: {response.status_code}")
                    print(f"Response texts: {response.text}")
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
                
                return self._parse_game_data(game_data)
            except Exception as e:
                print(f"Error in getting MobyGames game by ID: {e}")
                return None

    def _parse_game_data(self, game_data: Dict[str, Any]) -> MobyGamesGame:
        """Parse raw MobyGames game data into structured model"""
        # Parse alternate titles
        alternate_titles = []
        if game_data.get("alternate_titles"):
            for alt in game_data["alternate_titles"]:
                alternate_titles.append(MobyGamesAlternateTitle(
                    description=alt.get("description", ""),
                    title=alt.get("title", "")
                ))
        
        # Parse genres
        genres = []
        if game_data.get("genres"):
            for genre in game_data["genres"]:
                genres.append(MobyGamesGenre(
                    genre_category=genre.get("genre_category", ""),
                    genre_category_id=genre.get("genre_category_id", 0),
                    genre_id=genre.get("genre_id", 0),
                    genre_name=genre.get("genre_name", "")
                ))
        
        # Parse platforms
        platforms = []
        if game_data.get("platforms"):
            for platform in game_data["platforms"]:
                platforms.append(MobyGamesPlatform(
                    first_release_date=platform.get("first_release_date"),
                    platform_id=platform.get("platform_id", 0),
                    platform_name=platform.get("platform_name", "")
                ))
        
        # Parse cover
        sample_cover = None
        if game_data.get("sample_cover"):
            cover_data = game_data["sample_cover"]
            sample_cover = MobyGamesCover(
                height=cover_data.get("height", 0),
                image=cover_data.get("image", ""),
                platforms=cover_data.get("platforms", []),
                thumbnail_image=cover_data.get("thumbnail_image", ""),
                width=cover_data.get("width", 0)
            )
        
        # Parse screenshots
        sample_screenshots = []
        if game_data.get("sample_screenshots"):
            for screenshot in game_data["sample_screenshots"]:
                sample_screenshots.append(MobyGamesScreenshot(
                    caption=screenshot.get("caption", ""),
                    height=screenshot.get("height", 0),
                    image=screenshot.get("image", ""),
                    thumbnail_image=screenshot.get("thumbnail_image", ""),
                    width=screenshot.get("width", 0)
                ))
        
        return MobyGamesGame(
            game_id=game_data.get("game_id", 0),
            title=game_data.get("title", ""),
            description=game_data.get("description"),
            alternate_titles=alternate_titles if alternate_titles else None,
            genres=genres if genres else None,
            platforms=platforms if platforms else None,
            developers=game_data.get("developers", []),
            publishers=game_data.get("publishers", []),
            sample_cover=sample_cover,
            sample_screenshots=sample_screenshots if sample_screenshots else None,
            moby_score=game_data.get("moby_score"),
            num_votes=game_data.get("num_votes"),
            moby_url=game_data.get("moby_url"),
            official_url=game_data.get("official_url")
        )

    def _extract_platform_names(self, platforms_data: List[MobyGamesPlatform]) -> List[str]:
        """Extract platform names from MobyGames platform objects"""
        return [platform.platform_name for platform in platforms_data if platform.platform_name]

    def _extract_genre_names(self, genres_data: List[MobyGamesGenre]) -> List[str]:
        """Extract genre names from MobyGames genre objects"""
        return [genre.genre_name for genre in genres_data if genre.genre_name]

    def _extract_developer_names(self, developers_data: List[Dict[str, Any]]) -> List[str]:
        """Extract developer names from MobyGames data"""
        return [dev.get("company_name", "") for dev in developers_data if dev.get("company_name")]

    def _extract_publisher_names(self, publishers_data: List[Dict[str, Any]]) -> List[str]:
        """Extract publisher names from MobyGames data"""
        return [pub.get("company_name", "") for pub in publishers_data if pub.get("company_name")]

    def convert_to_game_model(self, mobygames_game: MobyGamesGame) -> Dict[str, Any]:
        """Convert MobyGames game to our game model format"""
        from datetime import datetime
        
        # Get earliest release date from platforms
        release_date = None
        if mobygames_game.platforms:
            earliest_date = None
            for platform in mobygames_game.platforms:
                if platform.first_release_date:
                    try:
                        # Handle different date formats
                        if len(platform.first_release_date) == 4:  # Just year
                            date_obj = datetime.strptime(platform.first_release_date, "%Y")
                        elif len(platform.first_release_date) == 7:  # Year-month
                            date_obj = datetime.strptime(platform.first_release_date, "%Y-%m")
                        else:  # Full date
                            date_obj = datetime.strptime(platform.first_release_date, "%Y-%m-%d")
                        
                        if earliest_date is None or date_obj < earliest_date:
                            earliest_date = date_obj
                    except ValueError:
                        continue
            
            release_date = earliest_date
        
        # Clean description from HTML tags
        clean_description = None
        if mobygames_game.description:
            clean_description = re.sub(r'<[^>]+>', '', mobygames_game.description)
            clean_description = clean_description.strip()
        
        return {
            "title": mobygames_game.title,
            "description": clean_description,
            "release_date": release_date.isoformat() if release_date else None,
            "platforms": self._extract_platform_names(mobygames_game.platforms or []),
            "genres": self._extract_genre_names(mobygames_game.genres or []),
            "developers": self._extract_developer_names(mobygames_game.developers or []),
            "publishers": self._extract_publisher_names(mobygames_game.publishers or []),
            "cover_image_url": mobygames_game.sample_cover.image if mobygames_game.sample_cover else None,
            "rating": mobygames_game.moby_score,
            "mobygames_id": mobygames_game.game_id,
            "alternate_titles": [alt.title for alt in mobygames_game.alternate_titles or []],
            "moby_url": mobygames_game.moby_url,
            "official_url": mobygames_game.official_url,
            "num_votes": mobygames_game.num_votes,
            "screenshots": [screenshot.image for screenshot in mobygames_game.sample_screenshots or []]
        }

    def convert_to_woocommerce_product(self, mobygames_game: MobyGamesGame, price: float = 29.99) -> Dict[str, Any]:
        """Convert MobyGames game to WooCommerce product format"""
        from services.woocommerce_service import WooCommerceService
        
        # Get basic game data
        game_data = self.convert_to_game_model(mobygames_game)
        
        # Use WooCommerce service to create product data
        woocommerce_service = WooCommerceService()
        product_data = woocommerce_service.create_game_product_data({
            **game_data,
            "price": price
        })
        
        # Enhance with MobyGames-specific data
        if mobygames_game.sample_cover:
            product_data["images"] = [{
                "src": mobygames_game.sample_cover.image,
                "name": f"{mobygames_game.title} - Cover",
                "alt": f"{mobygames_game.title} game cover"
            }]
        
        # Add screenshots as additional images
        if mobygames_game.sample_screenshots:
            for i, screenshot in enumerate(mobygames_game.sample_screenshots[:4]):  # Limit to 4 screenshots
                product_data["images"].append({
                    "src": screenshot.image,
                    "name": f"{mobygames_game.title} - Screenshot {i+1}",
                    "alt": screenshot.caption or f"{mobygames_game.title} screenshot {i+1}"
                })
        
        # Add MobyGames-specific metadata
        product_data["meta_data"].extend([
            {
                "key": "_mobygames_id",
                "value": str(mobygames_game.game_id)
            },
            {
                "key": "_mobygames_url",
                "value": mobygames_game.moby_url or ""
            },
            {
                "key": "_mobygames_score",
                "value": str(mobygames_game.moby_score or 0)
            },
            {
                "key": "_mobygames_votes",
                "value": str(mobygames_game.num_votes or 0)
            },
            {
                "key": "_alternate_titles",
                "value": ", ".join([alt.title for alt in mobygames_game.alternate_titles or []])
            }
        ])
        
        # Add genre categories as tags
        if mobygames_game.genres:
            for genre in mobygames_game.genres:
                product_data["tags"].append({
                    "name": f"{genre.genre_category}: {genre.genre_name}".lower().replace(" ", "-")
                })
        
        return product_data
