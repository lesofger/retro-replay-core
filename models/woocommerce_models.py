from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ProductImage(BaseModel):
    src: str
    name: str
    alt: str

class ProductCategory(BaseModel):
    id: Optional[int] = None
    name: str
    slug: Optional[str] = None

class ProductTag(BaseModel):
    id: Optional[int] = None
    name: str
    slug: Optional[str] = None

class ProductDimensions(BaseModel):
    length: str = "10"
    width: str = "7"
    height: str = "1"

class ProductMetaData(BaseModel):
    id: Optional[int] = None
    key: str
    value: str

class WooCommerceProductCreate(BaseModel):
    name: str = Field(..., description="Product name")
    type: str = Field(default="simple", description="Product type")
    regular_price: str = Field(..., description="Regular price")
    description: Optional[str] = Field(None, description="Product description")
    short_description: Optional[str] = Field(None, description="Short description")
    categories: Optional[List[ProductCategory]] = Field(default_factory=list)
    tags: Optional[List[ProductTag]] = Field(default_factory=list)
    images: Optional[List[ProductImage]] = Field(default_factory=list)
    manage_stock: bool = Field(default=True)
    stock_quantity: int = Field(default=10)
    stock_status: str = Field(default="instock")
    weight: str = Field(default="0.1")
    dimensions: Optional[ProductDimensions] = Field(default_factory=ProductDimensions)
    shipping_class: str = Field(default="")
    reviews_allowed: bool = Field(default=True)
    purchase_note: Optional[str] = Field(None)
    menu_order: int = Field(default=0)
    meta_data: Optional[List[ProductMetaData]] = Field(default_factory=list)

class WooCommerceProductUpdate(BaseModel):
    name: Optional[str] = None
    regular_price: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    categories: Optional[List[ProductCategory]] = None
    tags: Optional[List[ProductTag]] = None
    images: Optional[List[ProductImage]] = None
    manage_stock: Optional[bool] = None
    stock_quantity: Optional[int] = None
    stock_status: Optional[str] = None
    weight: Optional[str] = None
    dimensions: Optional[ProductDimensions] = None
    shipping_class: Optional[str] = None
    reviews_allowed: Optional[bool] = None
    purchase_note: Optional[str] = None
    menu_order: Optional[int] = None
    meta_data: Optional[List[ProductMetaData]] = None

class WooCommerceProduct(BaseModel):
    id: int
    name: str
    slug: str
    permalink: str
    date_created: datetime
    date_modified: datetime
    type: str
    status: str
    featured: bool
    catalog_visibility: str
    description: str
    short_description: str
    sku: str
    price: str
    regular_price: str
    sale_price: str
    date_on_sale_from: Optional[datetime] = None
    date_on_sale_to: Optional[datetime] = None
    on_sale: bool
    purchasable: bool
    total_sales: int
    virtual: bool
    downloadable: bool
    downloads: List[Any] = Field(default_factory=list)
    download_limit: int
    download_expiry: int
    external_url: str
    button_text: str
    tax_status: str
    tax_class: str
    manage_stock: bool
    stock_quantity: Optional[int] = None
    stock_status: str
    backorders: str
    backorders_allowed: bool
    backordered: bool
    sold_individually: bool
    weight: str
    dimensions: ProductDimensions
    shipping_required: bool
    shipping_taxable: bool
    shipping_class: str
    shipping_class_id: int
    reviews_allowed: bool
    average_rating: str
    rating_count: int
    related_ids: List[int] = Field(default_factory=list)
    upsell_ids: List[int] = Field(default_factory=list)
    cross_sell_ids: List[int] = Field(default_factory=list)
    parent_id: int
    purchase_note: str
    categories: List[ProductCategory] = Field(default_factory=list)
    tags: List[ProductTag] = Field(default_factory=list)
    images: List[ProductImage] = Field(default_factory=list)
    attributes: List[Any] = Field(default_factory=list)
    default_attributes: List[Any] = Field(default_factory=list)
    variations: List[int] = Field(default_factory=list)
    grouped_products: List[int] = Field(default_factory=list)
    menu_order: int
    meta_data: List[ProductMetaData] = Field(default_factory=list)

class GameToProductRequest(BaseModel):
    title: str = Field(..., description="Game title")
    description: Optional[str] = Field(None, description="Game description")
    platforms: List[str] = Field(default_factory=list, description="Game platforms")
    genres: List[str] = Field(default_factory=list, description="Game genres")
    release_date: Optional[str] = Field(None, description="Release date")
    developer: Optional[str] = Field(None, description="Game developer")
    publisher: Optional[str] = Field(None, description="Game publisher")
    price: float = Field(default=29.99, description="Product price")
    stock_quantity: int = Field(default=10, description="Stock quantity")

class ProductResponse(BaseModel):
    success: bool
    message: str
    product_id: Optional[int] = None
    product_data: Optional[Dict[str, Any]] = None

class ProductListResponse(BaseModel):
    success: bool
    products: List[WooCommerceProduct]
    total: int
    page: int
    per_page: int
