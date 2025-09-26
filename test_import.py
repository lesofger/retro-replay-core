"""
Test script for MobyGames import functionality
Run this to test importing MobyGames data to WooCommerce
"""

import asyncio
import httpx
import json
from services.import_service import ImportService

async def test_import_api():
    """Test the MobyGames import API endpoints"""
    print("🎮 Testing MobyGames Import API")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # Test 1: Quick import a single game
        print("\n1. Testing quick import of a single game...")
        try:
            response = await client.post(
                f"{base_url}/import/mobygames/quick-import",
                params={
                    "mobygames_id": 1,  # The X-Files Game
                    "price": 39.99,
                    "stock_quantity": 15
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Quick import successful!")
                print(f"   Game: {result.get('message', 'Unknown')}")
                print(f"   WooCommerce ID: {result.get('woocommerce_product_id')}")
                print(f"   URL: {result.get('woocommerce_url')}")
            else:
                print(f"❌ Quick import failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Quick import error: {e}")
        
        # Test 2: Import with detailed request
        print("\n2. Testing detailed import request...")
        try:
            import_request = {
                "mobygames_id": 2,  # Another game
                "price": 29.99,
                "stock_quantity": 10,
                "category": "Retro Games"
            }
            
            response = await client.post(
                f"{base_url}/import/mobygames/single",
                json=import_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Detailed import successful!")
                print(f"   Game: {result.get('game_title')}")
                print(f"   Price: ${result.get('price')}")
                print(f"   Stock: {result.get('stock_quantity')}")
                print(f"   Category: {result.get('category')}")
                print(f"   Moby Score: {result.get('moby_score')}")
                print(f"   Platforms: {result.get('platforms')}")
            else:
                print(f"❌ Detailed import failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Detailed import error: {e}")
        
        # Test 3: Bulk import
        print("\n3. Testing bulk import...")
        try:
            bulk_request = {
                "mobygames_ids": [3, 4, 5],  # Multiple games
                "price": 24.99,
                "stock_quantity": 8,
                "category": "Retro Games",
                "delay_between_imports": 0.5
            }
            
            response = await client.post(
                f"{base_url}/import/mobygames/bulk",
                json=bulk_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Bulk import completed!")
                print(f"   Summary: {result.get('message')}")
                summary = result.get('summary', {})
                print(f"   Total: {summary.get('total')}")
                print(f"   Successful: {summary.get('successful')}")
                print(f"   Failed: {summary.get('failed')}")
                print(f"   Success Rate: {summary.get('success_rate')}")
            else:
                print(f"❌ Bulk import failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Bulk import error: {e}")
        
        # Test 4: Search and import
        print("\n4. Testing search and import...")
        try:
            search_request = {
                "search_query": "mario",
                "limit": 3,
                "price": 19.99,
                "stock_quantity": 12,
                "category": "Retro Games"
            }
            
            response = await client.post(
                f"{base_url}/import/mobygames/search",
                json=search_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Search and import completed!")
                print(f"   Summary: {result.get('message')}")
                summary = result.get('summary', {})
                print(f"   Total: {summary.get('total')}")
                print(f"   Successful: {summary.get('successful')}")
            else:
                print(f"❌ Search and import failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Search and import error: {e}")
        
        # Test 5: Check import status
        print("\n5. Testing import status check...")
        try:
            response = await client.get(f"{base_url}/import/mobygames/1/status")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Status check successful!")
                print(f"   Game: {result.get('game_title')}")
                print(f"   Imported: {result.get('imported')}")
                if result.get('imported'):
                    print(f"   WooCommerce ID: {result.get('woocommerce_product_id')}")
                    print(f"   URL: {result.get('woocommerce_url')}")
            else:
                print(f"❌ Status check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Status check error: {e}")
        
        # Test 6: Get import history
        print("\n6. Testing import history...")
        try:
            response = await client.get(f"{base_url}/import/mobygames/history?limit=10")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Import history retrieved!")
                print(f"   Total imported: {result.get('total_imported')}")
                games = result.get('games', [])
                for i, game in enumerate(games[:3], 1):  # Show first 3
                    print(f"   {i}. {game.get('title')} (ID: {game.get('woocommerce_product_id')}) - ${game.get('price')}")
            else:
                print(f"❌ Import history failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Import history error: {e}")
        
        # Test 7: Get import statistics
        print("\n7. Testing import statistics...")
        try:
            response = await client.get(f"{base_url}/import/mobygames/stats")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Import statistics retrieved!")
                stats = result.get('stats', {})
                print(f"   Total imported: {stats.get('total_imported')}")
                print(f"   Average price: ${stats.get('average_price')}")
                print(f"   Total stock: {stats.get('total_stock_value')}")
                print(f"   Recent imports: {stats.get('recent_imports')}")
            else:
                print(f"❌ Import statistics failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Import statistics error: {e}")

async def test_direct_import_service():
    """Test the import service directly"""
    print("\n" + "=" * 60)
    print("🔧 Testing Import Service Directly")
    print("=" * 60)
    
    import_service = ImportService()
    
    # Test direct import
    print("\n1. Testing direct service import...")
    try:
        result = await import_service.import_single_game(
            mobygames_id=1,
            price=35.99,
            stock_quantity=20,
            category="Test Games"
        )
        
        if result["success"]:
            print(f"✅ Direct import successful!")
            print(f"   Game: {result['game_title']}")
            print(f"   WooCommerce ID: {result['woocommerce_product_id']}")
            print(f"   Price: ${result['price']}")
            print(f"   Stock: {result['stock_quantity']}")
        else:
            print(f"❌ Direct import failed: {result['error']}")
    except Exception as e:
        print(f"❌ Direct import error: {e}")
    
    # Test status check
    print("\n2. Testing direct status check...")
    try:
        result = await import_service.get_import_status(1)
        
        if result["success"]:
            print(f"✅ Status check successful!")
            print(f"   Game: {result['game_title']}")
            print(f"   Imported: {result['imported']}")
            if result.get('woocommerce_product_id'):
                print(f"   WooCommerce ID: {result['woocommerce_product_id']}")
        else:
            print(f"❌ Status check failed: {result['error']}")
    except Exception as e:
        print(f"❌ Status check error: {e}")

async def main():
    """Run all tests"""
    print("Starting MobyGames Import API tests...")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print("Press Ctrl+C to cancel")
    
    try:
        await test_import_api()
        await test_direct_import_service()
        
        print("\n" + "=" * 60)
        print("🎮 All import tests completed!")
        print("\nNext steps:")
        print("1. Check your WooCommerce store for imported products")
        print("2. Visit http://localhost:8000/docs for API documentation")
        print("3. Use the import endpoints in your applications")
        
    except KeyboardInterrupt:
        print("\nTests cancelled by user")
    except Exception as e:
        print(f"\nTests failed with error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
