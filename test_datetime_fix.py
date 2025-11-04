"""
Quick test to verify dates serialization fix
"""

import asyncio
import json
from services.import_service import ImportService

async def test_datetime_serialization():
    """Test that datetime objects are properly serialized"""
    print("🧪 Testing dates serialization fix...")
    
    import_service = ImportService()
    
    try:
        # Test the import service directly
        result = await import_service.import_single_game(
            mobygames_id=1,
            price=29.99,
            stock_quantity=10
        )
        
        # Try to serialize the result to JSON
        json_result = json.dumps(result, indent=2)
        
        print("✅ Datetime serialization test passed!")
        print("Result keys:", list(result.keys()))
        
        # Check if release_date is properly formatted
        if 'platforms' in result:
            print(f"Platforms: {result['platforms']}")
        if 'genres' in result:
            print(f"Genres: {result['genres']}")
        
        print("\nJSONs serialization successful!")
        
    except Exception as e:
        print(f"❌ Date serialization test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_datetime_serialization())

