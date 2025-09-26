from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict, Any
from services.woocommerce_service import WooCommerceService
from models.woocommerce_models import (
    WooCommerceProductCreate,
    WooCommerceProductUpdate,
    WooCommerceProduct,
    GameToProductRequest,
    ProductResponse,
    ProductListResponse
)
import json

router = APIRouter(prefix="/woocommerce", tags=["woocommerce"])

# Initialize WooCommerce service
woocommerce_service = WooCommerceService()

@router.post("/products", response_model=ProductResponse)
async def create_product(product: WooCommerceProductCreate):
    """Create a new product in WooCommerce"""
    try:
        product_data = product.dict()
        result = await woocommerce_service.create_product(product_data)
        
        return ProductResponse(
            success=True,
            message="Product created successfully",
            product_id=result.get("id"),
            product_data=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/products/game", response_model=ProductResponse)
async def create_game_product(game_request: GameToProductRequest):
    """Create a WooCommerce product from game data"""
    try:
        # Convert game data to product format
        game_data = game_request.dict()
        product_data = woocommerce_service.create_game_product_data(game_data)
        
        # Create the product
        result = await woocommerce_service.create_product(product_data)
        
        return ProductResponse(
            success=True,
            message=f"Game product '{game_request.title}' created successfully",
            product_id=result.get("id"),
            product_data=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/products/{product_id}", response_model=WooCommerceProduct)
async def get_product(product_id: int):
    """Get a specific product by ID"""
    try:
        result = await woocommerce_service.get_product(product_id)
        return WooCommerceProduct(**result)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/products", response_model=ProductListResponse)
async def get_products(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    category: Optional[str] = Query(None, description="Category filter"),
    status: Optional[str] = Query("publish", description="Product status"),
    featured: Optional[bool] = Query(None, description="Featured products only")
):
    """Get all products with optional filters"""
    try:
        params = {
            "page": page,
            "per_page": per_page,
            "status": status
        }
        
        if search:
            params["search"] = search
        if category:
            params["category"] = category
        if featured is not None:
            params["featured"] = featured
        
        result = await woocommerce_service.get_products(params)
        
        # Convert to our model format
        products = [WooCommerceProduct(**product) for product in result]
        
        return ProductListResponse(
            success=True,
            products=products,
            total=len(products),
            page=page,
            per_page=per_page
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_update: WooCommerceProductUpdate):
    """Update an existing product"""
    try:
        update_data = product_update.dict(exclude_unset=True)
        result = await woocommerce_service.update_product(product_id, update_data)
        
        return ProductResponse(
            success=True,
            message="Product updated successfully",
            product_id=product_id,
            product_data=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/products/{product_id}", response_model=ProductResponse)
async def delete_product(product_id: int, force: bool = Query(False, description="Force delete")):
    """Delete a product"""
    try:
        result = await woocommerce_service.delete_product(product_id)
        
        return ProductResponse(
            success=True,
            message="Product deleted successfully",
            product_id=product_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/categories")
async def get_categories():
    """Get all product categories"""
    try:
        categories = await woocommerce_service.get_categories()
        return {"success": True, "categories": categories}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tags")
async def get_tags():
    """Get all product tags"""
    try:
        tags = await woocommerce_service.get_tags()
        return {"success": True, "tags": tags}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/test-connection")
async def test_connection():
    """Test WooCommerce API connection"""
    try:
        # Try to get products with minimal data
        result = await woocommerce_service.get_products({"per_page": 1})
        return {
            "success": True,
            "message": "WooCommerce API connection successful",
            "store_url": woocommerce_service.base_url
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Connection failed: {str(e)}")

@router.post("/bulk-create-games")
async def bulk_create_game_products(games: List[GameToProductRequest]):
    """Create multiple game products at once"""
    results = []
    
    for game_request in games:
        try:
            # Convert game data to product format
            game_data = game_request.dict()
            product_data = woocommerce_service.create_game_product_data(game_data)
            
            # Create the product
            result = await woocommerce_service.create_product(product_data)
            
            results.append({
                "success": True,
                "game_title": game_request.title,
                "product_id": result.get("id"),
                "message": f"Product created successfully"
            })
        except Exception as e:
            results.append({
                "success": False,
                "game_title": game_request.title,
                "error": str(e)
            })
    
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    return {
        "success": True,
        "message": f"Bulk operation completed: {successful} successful, {failed} failed",
        "results": results,
        "summary": {
            "total": len(results),
            "successful": successful,
            "failed": failed
        }
    }
