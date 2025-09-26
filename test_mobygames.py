"""
Test script for MobyGames integration
Run this to test the enhanced MobyGames API integration
"""

import asyncio
import httpx
from services.mobygames_service import MobyGamesService

async def test_mobygames_api():
    """Test the enhanced MobyGames API integration"""
    print("🎮 Testing Enhanced MobyGames Integration")
    print("=" * 60)
    
    mobygames_service = MobyGamesService()
    
    # Test 1: Search for games
    print("\n1. Testing MobyGames search...")
    try:
        games = await mobygames_service.search_games("x-files", limit=3)
        print(f"✅ Found {len(games)} games")
        
        for i, game in enumerate(games, 1):
            print(f"   {i}. {game.title} (ID: {game.game_id})")
            print(f"      Platforms: {[p.platform_name for p in game.platforms or []]}")
            print(f"      Genres: {[g.genre_name for g in game.genres or []]}")
            print(f"      Moby Score: {game.moby_score}")
            if game.sample_cover:
                print(f"      Cover: {game.sample_cover.image}")
            print()
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return
    
    # Test 2: Get specific game details
    if games:
        print("\n2. Testing detailed game fetch...")
        try:
            game_id = games[0].game_id
            detailed_game = await mobygames_service.get_game_by_id(game_id)
            
            if detailed_game:
                print(f"✅ Retrieved detailed info for '{detailed_game.title}'")
                print(f"   Description: {detailed_game.description[:100]}..." if detailed_game.description else "   No description")
                print(f"   Alternate titles: {len(detailed_game.alternate_titles or [])}")
                print(f"   Screenshots: {len(detailed_game.sample_screenshots or [])}")
                print(f"   Moby URL: {detailed_game.moby_url}")
                print(f"   Official URL: {detailed_game.official_url}")
            else:
                print("❌ Failed to get detailed game info")
        except Exception as e:
            print(f"❌ Detailed fetch failed: {e}")
    
    # Test 3: Convert to game model
    if games:
        print("\n3. Testing game model conversion...")
        try:
            game = games[0]
            game_model = mobygames_service.convert_to_game_model(game)
            
            print(f"✅ Converted '{game.title}' to game model")
            print(f"   Title: {game_model['title']}")
            print(f"   Platforms: {game_model['platforms']}")
            print(f"   Genres: {game_model['genres']}")
            print(f"   Developers: {game_model['developers']}")
            print(f"   Publishers: {game_model['publishers']}")
            print(f"   Rating: {game_model['rating']}")
            print(f"   MobyGames ID: {game_model['mobygames_id']}")
            print(f"   Alternate titles: {game_model['alternate_titles']}")
            print(f"   Screenshots: {len(game_model['screenshots'])}")
        except Exception as e:
            print(f"❌ Game model conversion failed: {e}")
    
    # Test 4: Convert to WooCommerce product
    if games:
        print("\n4. Testing WooCommerce product conversion...")
        try:
            game = games[0]
            product_data = mobygames_service.convert_to_woocommerce_product(game, price=39.99)
            
            print(f"✅ Converted '{game.title}' to WooCommerce product")
            print(f"   Product name: {product_data['name']}")
            print(f"   Price: ${product_data['regular_price']}")
            print(f"   Categories: {[cat['name'] for cat in product_data['categories']]}")
            print(f"   Tags: {[tag['name'] for tag in product_data['tags'][:5]]}")  # Show first 5 tags
            print(f"   Images: {len(product_data['images'])}")
            print(f"   Meta data fields: {len(product_data['meta_data'])}")
            
            # Show some metadata
            for meta in product_data['meta_data'][:3]:
                print(f"      {meta['key']}: {meta['value']}")
        except Exception as e:
            print(f"❌ WooCommerce conversion failed: {e}")
    
    # Test 5: Test API endpoints
    print("\n5. Testing API endpoints...")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        try:
            # Test search endpoint
            response = await client.get(f"{base_url}/games/search/mobygames?query=x-files&limit=2")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Search endpoint working - found {len(data)} games")
            else:
                print(f"❌ Search endpoint failed: {response.status_code}")
            
            # Test specific game endpoint
            if games:
                game_id = games[0].game_id
                response = await client.get(f"{base_url}/games/mobygames/{game_id}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Game detail endpoint working - retrieved '{data['title']}'")
                else:
                    print(f"❌ Game detail endpoint failed: {response.status_code}")
            
        except Exception as e:
            print(f"❌ API endpoint test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎮 MobyGames integration test completed!")
    print("\nNext steps:")
    print("1. Test importing games to WooCommerce:")
    print(f"   curl -X POST http://localhost:8000/games/mobygames/{games[0].game_id if games else 'GAME_ID'}/import")
    print("2. Test bulk import:")
    print("   curl -X POST http://localhost:8000/games/mobygames/bulk-import -H 'Content-Type: application/json' -d '[1, 2, 3]'")
    print("3. Check your WooCommerce store for imported products")

if __name__ == "__main__":
    print("Starting MobyGames API test...")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print("Press Ctrl+C to cancel")
    
    try:
        asyncio.run(test_mobygames_api())
    except KeyboardInterrupt:
        print("\nTest cancelled by user")
    except Exception as e:
        print(f"\nTest failed with error: {e}")
