"""
Test script for WooCommerce integration
Run this to test creating products in your WooCommerce store
"""

import asyncio
import httpx
from data.mock_games import get_mock_games, get_random_game

async def test_woocommerce_api():
    """Test the WooCommerce API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🎮 Testing WooCommerce Integration for Retro Replay Core")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        # Test 1: Test connection
        print("\n1. Testing WooCommerce connection...")
        try:
            response = await client.post(f"{base_url}/woocommerce/test-connection")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Connection successful: {result['message']}")
                print(f"   Store URL: {result['store_url']}")
            else:
                print(f"❌ Connection failed: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return
        
        # Test 2: Create a single game product
        print("\n2. Creating a single game product...")
        random_game = get_random_game()
        print(f"   Creating product for: {random_game['title']}")
        
        try:
            response = await client.post(
                f"{base_url}/woocommerce/products/game",
                json=random_game
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Product created successfully!")
                print(f"   Product ID: {result['product_id']}")
                print(f"   Message: {result['message']}")
            else:
                print(f"❌ Failed to create product: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Error creating product: {e}")
        
        # Test 3: Get products
        print("\n3. Fetching products from WooCommerce...")
        try:
            response = await client.get(f"{base_url}/woocommerce/products?per_page=5")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Found {result['total']} products")
                for product in result['products'][:3]:  # Show first 3
                    print(f"   - {product['name']} (ID: {product['id']}) - ${product['regular_price']}")
            else:
                print(f"❌ Failed to fetch products: {response.status_code}")
        except Exception as e:
            print(f"❌ Error fetching products: {e}")
        
        # Test 4: Bulk create multiple games
        print("\n4. Creating multiple game products...")
        sample_games = get_mock_games()[:3]  # First 3 games
        
        try:
            response = await client.post(
                f"{base_url}/woocommerce/bulk-create-games",
                json=sample_games
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Bulk operation completed!")
                print(f"   Total: {result['summary']['total']}")
                print(f"   Successful: {result['summary']['successful']}")
                print(f"   Failed: {result['summary']['failed']}")
                
                for item in result['results']:
                    if item['success']:
                        print(f"   ✅ {item['game_title']} - Product ID: {item['product_id']}")
                    else:
                        print(f"   ❌ {item['game_title']} - Error: {item['error']}")
            else:
                print(f"❌ Bulk operation failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error in bulk operation: {e}")
        
        # Test 5: Get categories and tags
        print("\n5. Fetching categories and tags...")
        try:
            # Get categories
            response = await client.get(f"{base_url}/woocommerce/categories")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Found {len(result['categories'])} categories")
                for cat in result['categories'][:3]:
                    print(f"   - {cat['name']} (ID: {cat['id']})")
            
            # Get tags
            response = await client.get(f"{base_url}/woocommerce/tags")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Found {len(result['tags'])} tags")
                for tag in result['tags'][:5]:
                    print(f"   - {tag['name']} (ID: {tag['id']})")
        except Exception as e:
            print(f"❌ Error fetching categories/tags: {e}")
    
    print("\n" + "=" * 60)
    print("🎮 WooCommerce integration test completed!")
    print("\nNext steps:")
    print("1. Check your WooCommerce store at https://retro-replay.com/wp-admin")
    print("2. Go to Products to see the created items")
    print("3. Use the API documentation at http://localhost:8000/docs")

if __name__ == "__main__":
    print("Starting WooCommerce API test...")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print("Press Ctrl+C to cancel")
    
    try:
        asyncio.run(test_woocommerce_api())
    except KeyboardInterrupt:
        print("\nTest cancelled by user")
    except Exception as e:
        print(f"\nTest failed with error: {e}")
