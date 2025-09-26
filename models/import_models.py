from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ImportRequest(BaseModel):
    mobygames_id: int = Field(..., description="MobyGames game ID to import")
    price: float = Field(default=29.99, ge=0, description="Product price")
    stock_quantity: int = Field(default=10, ge=0, description="Stock quantity")
    category: str = Field(default="Retro Games", description="Product category")

class BulkImportRequest(BaseModel):
    mobygames_ids: List[int] = Field(..., description="List of MobyGames game IDs to import")
    price: float = Field(default=29.99, ge=0, description="Product price")
    stock_quantity: int = Field(default=10, ge=0, description="Stock quantity")
    category: str = Field(default="Retro Games", description="Product category")
    delay_between_imports: float = Field(default=1.0, ge=0, le=10, description="Delay between imports in seconds")

class SearchImportRequest(BaseModel):
    search_query: str = Field(..., description="Search query for games")
    limit: int = Field(default=5, ge=1, le=20, description="Maximum number of games to import")
    price: float = Field(default=29.99, ge=0, description="Product price")
    stock_quantity: int = Field(default=10, ge=0, description="Stock quantity")
    category: str = Field(default="Retro Games", description="Product category")

class ImportResult(BaseModel):
    success: bool
    mobygames_id: int
    game_title: Optional[str] = None
    woocommerce_product_id: Optional[int] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    category: Optional[str] = None
    moby_score: Optional[float] = None
    platforms: Optional[List[str]] = None
    genres: Optional[List[str]] = None
    error: Optional[str] = None
    timestamp: str

class ImportResponse(BaseModel):
    success: bool
    message: str
    mobygames_id: Optional[int] = None
    game_title: Optional[str] = None
    woocommerce_product_id: Optional[int] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    category: Optional[str] = None
    moby_score: Optional[float] = None
    platforms: Optional[List[str]] = None
    genres: Optional[List[str]] = None
    woocommerce_url: Optional[str] = None
    error: Optional[str] = None
    timestamp: str

class BulkImportResponse(BaseModel):
    success: bool
    message: str
    summary: Dict[str, Any]
    results: List[ImportResult]
    timestamp: str

class ImportStatusResponse(BaseModel):
    success: bool
    imported: bool
    mobygames_id: int
    game_title: str
    woocommerce_product_id: Optional[int] = None
    woocommerce_url: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None
    timestamp: str

class ImportHistoryItem(BaseModel):
    woocommerce_product_id: int
    mobygames_id: str
    title: str
    price: str
    stock_quantity: Optional[int] = None
    date_created: str
    woocommerce_url: str

class ImportHistoryResponse(BaseModel):
    success: bool
    total_imported: int
    games: List[ImportHistoryItem]
    error: Optional[str] = None
    timestamp: str

class ImportStatsResponse(BaseModel):
    success: bool
    stats: Dict[str, Any]
    error: Optional[str] = None
    timestamp: str
