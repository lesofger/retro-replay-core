import httpx
import base64
from typing import Dict, List, Optional, Any
from config import settings
import json

class WooCommerceService:
    def __init__(self):
        self.base_url = settings.WOOCOMMERCE_URL
        self.consumer_key = settings.WOOCOMMERCE_CONSUMER_KEY
        self.consumer_secret = settings.WOOCOMMERCE_CONSUMER_SECRET
        self.api_url = f"{self.base_url}/wp-json/wc/v3"
        
    def _get_auth_header(self) -> str:
        """Generate Basic Auth header for WooCommerce API"""
        credentials = f"{self.consumer_key}:{self.consumer_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make authenticated request to WooCommerce API"""
        url = f"{self.api_url}/{endpoint}"
        headers = {
            "Authorization": self._get_auth_header(),
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, headers=headers, params=data)
                elif method.upper() == "POST":
                    response = await client.post(url, headers=headers, json=data)
                elif method.upper() == "PUT":
                    response = await client.put(url, headers=headers, json=data)
                elif method.upper() == "DELETE":
                    response = await client.delete(url, headers=headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                error_detail = f"WooCommerce API error: {e.response.status_code}"
                try:
                    error_data = e.response.json()
                    if "message" in error_data:
                        error_detail += f" - {error_data['message']}"
                except:
                    pass
                raise Exception(error_detail)
            except Exception as e:
                raise Exception(f"Request failed: {str(e)}")
    
    async def create_product(self, product_data: Dict) -> Dict:
        """Create a new product in WooCommerce"""
        return await self._make_request("POST", "products", product_data)
    
    async def get_product(self, product_id: int) -> Dict:
        """Get a product by ID"""
        return await self._make_request("GET", f"products/{product_id}")
    
    async def get_products(self, params: Optional[Dict] = None) -> List[Dict]:
        """Get all products with optional filters"""
        if params is None:
            params = {}
        return await self._make_request("GET", "products", params)
    
    async def update_product(self, product_id: int, product_data: Dict) -> Dict:
        """Update an existing product"""
        return await self._make_request("PUT", f"products/{product_id}", product_data)
    
    async def delete_product(self, product_id: int) -> Dict:
        """Delete a product"""
        return await self._make_request("DELETE", f"products/{product_id}")
    
    async def get_categories(self) -> List[Dict]:
        """Get all product categories"""
        return await self._make_request("GET", "products/categories")
    
    async def create_category(self, category_data: Dict) -> Dict:
        """Create a new product category"""
        return await self._make_request("POST", "products/categories", category_data)
    
    async def get_tags(self) -> List[Dict]:
        """Get all product tags"""
        return await self._make_request("GET", "products/tags")
    
    async def create_tag(self, tag_data: Dict) -> Dict:
        """Create a new product tag"""
        return await self._make_request("POST", "products/tags", tag_data)
    
    def create_game_product_data(self, game_data: Dict) -> Dict:
        """Convert game data to WooCommerce product format"""
        # Extract game information
        title = game_data.get("title", "Unknown Game")
        description = game_data.get("description", "")
        platforms = game_data.get("platforms", [])
        genres = game_data.get("genres", [])
        release_date = game_data.get("release_date", "")
        developer = game_data.get("developer", "")
        publisher = game_data.get("publisher", "")
        price = game_data.get("price", 29.99)
        
        # Create product description
        product_description = f"<h3>{title}</h3>"
        if description:
            product_description += f"<p>{description}</p>"
        
        if platforms:
            platform_list = ", ".join(platforms)
            product_description += f"<p><strong>Platforms:</strong> {platform_list}</p>"
        
        if genres:
            genre_list = ", ".join(genres)
            product_description += f"<p><strong>Genres:</strong> {genre_list}</p>"
        
        if developer:
            product_description += f"<p><strong>Developer:</strong> {developer}</p>"
        
        if publisher:
            product_description += f"<p><strong>Publisher:</strong> {publisher}</p>"
        
        if release_date:
            product_description += f"<p><strong>Release Date:</strong> {release_date}</p>"
        
        # Create short description
        short_description = f"Retro gaming classic: {title}"
        if platforms:
            short_description += f" for {platforms[0]}"
        
        # Build product data
        product_data = {
            "name": title,
            "type": "simple",
            "regular_price": str(price),
            "description": product_description,
            "short_description": short_description,
            "categories": [
                {"name": "Retro Games"}
            ],
            "tags": [
                {"name": "retro"},
                {"name": "gaming"},
                {"name": "classic"}
            ],
            "images": [],
            "manage_stock": True,
            "stock_quantity": 10,
            "stock_status": "instock",
            "weight": "0.1",
            "dimensions": {
                "length": "10",
                "width": "7",
                "height": "1"
            },
            "shipping_class": "",
            "reviews_allowed": True,
            "purchase_note": "Thank you for your purchase! Enjoy this retro gaming classic.",
            "menu_order": 0,
            "meta_data": [
                {
                    "key": "_game_platforms",
                    "value": json.dumps(platforms)
                },
                {
                    "key": "_game_genres", 
                    "value": json.dumps(genres)
                },
                {
                    "key": "_game_developer",
                    "value": developer
                },
                {
                    "key": "_game_publisher",
                    "value": publisher
                },
                {
                    "key": "_game_release_date",
                    "value": release_date
                }
            ]
        }
        
        # Add platform-specific tags
        for platform in platforms:
            product_data["tags"].append({"name": platform.lower().replace(" ", "-")})
        
        # Add genre-specific tags
        for genre in genres:
            product_data["tags"].append({"name": genre.lower().replace(" ", "-")})
        
        return product_data
