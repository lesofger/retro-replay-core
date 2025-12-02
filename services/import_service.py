import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from services.mobygames_service import MobyGamesService
from services.woocommerce_service import WooCommerceService
from models.external_api_models import MobyGamesGame

class ImportService:
    def __init__(self):
        self.mobygames_service = MobyGamesService()
        self.woocommerce_service = WooCommerceService()
    
    async def import_single_game(
        self, 
        mobygames_id: int, 
        price: float = 29.99,
        stock_quantity: int = 10,
        category: str = "Retro Games"
    ) -> Dict[str, Any]:
        """Import a single MobyGames game to WooCommerce"""
        try:
            # Step 1: Fetch game from MobyGames
            print(f"Fetching game {mobygames_id} from MobyGames...")
            game = await self.mobygames_service.get_game_by_id(mobygames_id)
            
            if not game:
                return {
                    "success": False,
                    "mobygames_id": mobygames_id,
                    "error": "Game not found on MobyGames",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Step 2: Convert to WooCommerce product format
            print(f"Converting '{game.title}' to WooCommerce format...")
            product_data = self.mobygames_service.convert_to_woocommerce_product(game, price)
            
            # Override some settings
            product_data["stock_quantity"] = stock_quantity
            product_data["categories"] = [{"name": category}]
            
            # Step 3: Create product in WooCommerce
            print(f"Creating product '{game.title}' in WooCommerce...")
            result = await self.woocommerce_service.create_product(product_data)
            
            return {
                "success": True,
                "mobygames_id": mobygames_id,
                "game_title": game.title,
                "woocommerce_product_id": result.get("id"),
                "price": price,
                "stock_quantity": stock_quantity,
                "category": category,
                "moby_score": game.moby_score,
                "platforms": [p.platform_name for p in game.platforms or []],
                "genres": [g.genre_name for g in game.genres or []],
                "timestamp": datetime.now().isoformat(),
                "woocommerce_url": f"{self.woocommerce_service.base_url}/product/{result.get('slug', '')}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "mobygames_id": mobygames_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def import_multiple_games(
        self,
        mobygames_ids: List[int],
        price: float = 29.99,
        stock_quantity: int = 10,
        category: str = "Retro Games",
        delay_between_imports: float = 1.0
    ) -> Dict[str, Any]:
        """Import multiple MobyGames games to WooCommerce with delay between imports"""
        results = []
        successful = 0
        failed = 0
        
        print(f"Starting bulk import of {len(mobygames_ids)} games...")
        
        for i, mobygames_id in enumerate(mobygames_ids, 1):
            print(f"\n--- Importing game {i}/{len(mobygames_ids)} (ID: {mobygames_id}) ---")
            
            result = await self.import_single_game(
                mobygames_id=mobygames_id,
                price=price,
                stock_quantity=stock_quantity,
                category=category
            )
            
            results.append(result)
            
            if result["success"]:
                successful += 1
                print(f"✅ Success: {result['game_title']} (WooCommerce ID: {result['woocommerce_product_id']})")
            else:
                failed += 1
                print(f"❌ Failed: {result['error']}")
            
            # Add delay between imports to avoid rate limiting
            if i < len(mobygames_ids):
                print(f"Waiting {delay_between_imports}s before next import...")
                await asyncio.sleep(delay_between_imports)
        
        return {
            "success": True,
            "message": f"Bulk import completed: {successful} successful, {failed} failed",
            "summary": {
                "total": len(mobygames_ids),
                "successful": successful,
                "failed": failed,
                "success_rate": f"{(successful/len(mobygames_ids)*100):.1f}%"
            },
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    
    async def search_and_import(
        self,
        search_query: str,
        limit: int = 5,
        price: float = 29.99,
        stock_quantity: int = 10,
        category: str = "Retro Games"
    ) -> Dict[str, Any]:
        """Search for games on MobyGames and import them to WooCommerce"""
        try:
            # Step 1: Search for games
            print(f"Searching for '{search_query}' on MobyGames...")
            games = await self.mobygames_service.search_games(search_query, limit)
            
            if not games:
                return {
                    "success": False,
                    "error": f"No games found for query: {search_query}",
                    "timestamp": datetime.now().isoformat()
                }
            
            print(f"Found {len(games)} games, starting import...")
            
            # Step 2: Extract IDs and import
            mobygames_ids = [game.game_id for game in games]
            return await self.import_multiple_games(
                mobygames_ids=mobygames_ids,
                price=price,
                stock_quantity=stock_quantity,
                category=category
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_import_status(self, mobygames_id: int) -> Dict[str, Any]:
        """Check if a MobyGames game has been imported to WooCommerce"""
        try:
            # Get game info from MobyGames
            game = await self.mobygames_service.get_game_by_id(mobygames_id)
            if not game:
                return {
                    "success": False,
                    "error": "Game not found on MobyGames",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Search for existing product in WooCommerce by MobyGames ID
            products = await self.woocommerce_service.get_products({
                "search": game.title,
                "per_page": 10
            })
            
            # Check if any product has the MobyGames ID in metadata
            for product in products:
                for meta in product.get("meta_data", []):
                    if meta.get("key") == "_mobygames_id" and meta.get("value") == str(mobygames_id):
                        return {
                            "success": True,
                            "imported": True,
                            "mobygames_id": mobygames_id,
                            "game_title": game.title,
                            "woocommerce_product_id": product.get("id"),
                            "woocommerce_url": f"{self.woocommerce_service.base_url}/product/{product.get('slug', '')}",
                            "timestamp": datetime.now().isoformat()
                        }
            
            return {
                "success": True,
                "imported": False,
                "mobygames_id": mobygames_id,
                "game_title": game.title,
                "message": "Game nots yets imported to WooCommerce",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_import_history(self, limit: int = 50) -> Dict[str, Any]:
        """Get recently imported products from WooCommerce"""
        try:
            products = await self.woocommerce_service.get_products({
                "per_page": limit,
                "orderby": "date",
                "order": "desc"
            })
            
            imported_games = []
            for product in products:
                mobygames_id = None
                for meta in product.get("meta_data", []):
                    if meta.get("key") == "_mobygames_id":
                        mobygames_id = meta.get("value")
                        break
                
                if mobygames_id:
                    imported_games.append({
                        "woocommerce_product_id": product.get("id"),
                        "mobygames_id": mobygames_id,
                        "title": product.get("name"),
                        "price": product.get("regular_price"),
                        "stock_quantity": product.get("stock_quantity"),
                        "date_created": product.get("date_created"),
                        "woocommerce_url": f"{self.woocommerce_service.base_url}/product/{product.get('slug', '')}"
                    })
            
            return {
                "success": True,
                "total_imported": len(imported_games),
                "games": imported_games,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
