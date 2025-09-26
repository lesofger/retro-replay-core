from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import List, Optional
from services.import_service import ImportService
from models.import_models import (
    ImportRequest,
    BulkImportRequest,
    SearchImportRequest,
    ImportResponse,
    BulkImportResponse,
    ImportStatusResponse,
    ImportHistoryResponse,
    ImportStatsResponse
)

router = APIRouter(prefix="/import", tags=["import"])

# Initialize import service
import_service = ImportService()

@router.post("/mobygames/single", response_model=ImportResponse)
async def import_single_game(request: ImportRequest):
    """Import a single MobyGames game to WooCommerce"""
    try:
        result = await import_service.import_single_game(
            mobygames_id=request.mobygames_id,
            price=request.price,
            stock_quantity=request.stock_quantity,
            category=request.category
        )
        
        if result["success"]:
            return ImportResponse(**result)
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mobygames/bulk", response_model=BulkImportResponse)
async def import_multiple_games(request: BulkImportRequest):
    """Import multiple MobyGames games to WooCommerce"""
    try:
        result = await import_service.import_multiple_games(
            mobygames_ids=request.mobygames_ids,
            price=request.price,
            stock_quantity=request.stock_quantity,
            category=request.category,
            delay_between_imports=request.delay_between_imports
        )
        
        return BulkImportResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mobygames/search", response_model=BulkImportResponse)
async def search_and_import_games(request: SearchImportRequest):
    """Search for games on MobyGames and import them to WooCommerce"""
    try:
        result = await import_service.search_and_import(
            search_query=request.search_query,
            limit=request.limit,
            price=request.price,
            stock_quantity=request.stock_quantity,
            category=request.category
        )
        
        if result["success"]:
            return BulkImportResponse(**result)
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mobygames/{mobygames_id}/status", response_model=ImportStatusResponse)
async def get_import_status(mobygames_id: int):
    """Check if a MobyGames game has been imported to WooCommerce"""
    try:
        result = await import_service.get_import_status(mobygames_id)
        
        if result["success"]:
            return ImportStatusResponse(**result)
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mobygames/history", response_model=ImportHistoryResponse)
async def get_import_history(limit: int = Query(50, ge=1, le=100, description="Number of recent imports to return")):
    """Get recently imported products from WooCommerce"""
    try:
        result = await import_service.get_import_history(limit)
        
        if result["success"]:
            return ImportHistoryResponse(**result)
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mobygames/stats", response_model=ImportStatsResponse)
async def get_import_stats():
    """Get import statistics"""
    try:
        # Get import history to calculate stats
        history_result = await import_service.get_import_history(1000)  # Get more for stats
        
        if not history_result["success"]:
            raise HTTPException(status_code=400, detail=history_result["error"])
        
        games = history_result["games"]
        
        # Calculate statistics
        total_imported = len(games)
        
        # Price statistics
        prices = [float(game["price"]) for game in games if game["price"]]
        avg_price = sum(prices) / len(prices) if prices else 0
        
        # Stock statistics
        stock_quantities = [game["stock_quantity"] for game in games if game["stock_quantity"]]
        total_stock = sum(stock_quantities) if stock_quantities else 0
        
        # Platform/genre analysis (would need to fetch from WooCommerce metadata)
        stats = {
            "total_imported": total_imported,
            "average_price": round(avg_price, 2),
            "total_stock_value": total_stock,
            "recent_imports": len([g for g in games if g["date_created"]])  # Games with creation date
        }
        
        return ImportStatsResponse(
            success=True,
            stats=stats,
            timestamp=history_result["timestamp"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mobygames/quick-import")
async def quick_import_game(
    mobygames_id: int = Query(..., description="MobyGames game ID"),
    price: float = Query(29.99, ge=0, description="Product price"),
    stock_quantity: int = Query(10, ge=0, description="Stock quantity")
):
    """Quick import a single game with minimal parameters"""
    try:
        result = await import_service.import_single_game(
            mobygames_id=mobygames_id,
            price=price,
            stock_quantity=stock_quantity
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": f"Game '{result['game_title']}' imported successfully!",
                "woocommerce_product_id": result["woocommerce_product_id"],
                "woocommerce_url": result["woocommerce_url"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mobygames/batch-import")
async def batch_import_games(
    mobygames_ids: List[int],
    price: float = Query(29.99, ge=0, description="Product price"),
    stock_quantity: int = Query(10, ge=0, description="Stock quantity"),
    delay: float = Query(1.0, ge=0, le=10, description="Delay between imports in seconds")
):
    """Batch import multiple games with query parameters"""
    try:
        result = await import_service.import_multiple_games(
            mobygames_ids=mobygames_ids,
            price=price,
            stock_quantity=stock_quantity,
            delay_between_imports=delay
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/mobygames/{mobygames_id}")
async def remove_imported_game(mobygames_id: int):
    """Remove an imported game from WooCommerce"""
    try:
        # First check if the game is imported
        status_result = await import_service.get_import_status(mobygames_id)
        
        if not status_result["success"]:
            raise HTTPException(status_code=400, detail=status_result["error"])
        
        if not status_result["imported"]:
            raise HTTPException(status_code=404, detail="Game not found in WooCommerce")
        
        # Delete the product from WooCommerce
        woocommerce_service = import_service.woocommerce_service
        result = await woocommerce_service.delete_product(status_result["woocommerce_product_id"])
        
        return {
            "success": True,
            "message": f"Game '{status_result['game_title']}' removed from WooCommerce",
            "mobygames_id": mobygames_id,
            "woocommerce_product_id": status_result["woocommerce_product_id"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
