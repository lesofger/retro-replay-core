# MobyGames Import API Guide

This guide covers the comprehensive MobyGames import API that allows you to import game data directly into your WooCommerce store.

## 🚀 Overview

The Import API provides multiple ways to import MobyGames data into WooCommerce:

- **Single Game Import** - Import one game at a time
- **Bulk Import** - Import multiple games in one operation
- **Search & Import** - Search for games and import them
- **Status Tracking** - Check import status and history
- **Statistics** - View import analytics

## 📚 API Endpoints

### Base URL: `/import`

## 🎮 Single Game Import

### Quick Import
```http
POST /import/mobygames/quick-import
```

**Query Parameters:**
- `mobygames_id` (required): MobyGames game ID
- `price` (optional): Product price (default: 29.99)
- `stock_quantity` (optional): Stock quantity (default: 10)

**Example:**
```bash
curl -X POST "http://localhost:8000/import/mobygames/quick-import?mobygames_id=1&price=39.99&stock_quantity=15"
```

### Detailed Import
```http
POST /import/mobygames/single
```

**Request Body:**
```json
{
  "mobygames_id": 1,
  "price": 39.99,
  "stock_quantity": 15,
  "category": "Retro Games"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/import/mobygames/single \
  -H "Content-Type: application/json" \
  -d '{
    "mobygames_id": 1,
    "price": 39.99,
    "stock_quantity": 15,
    "category": "Retro Games"
  }'
```

## 📦 Bulk Import

### Import Multiple Games
```http
POST /import/mobygames/bulk
```

**Request Body:**
```json
{
  "mobygames_ids": [1, 2, 3, 4, 5],
  "price": 29.99,
  "stock_quantity": 10,
  "category": "Retro Games",
  "delay_between_imports": 1.0
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/import/mobygames/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "mobygames_ids": [1, 2, 3],
    "price": 24.99,
    "stock_quantity": 8,
    "delay_between_imports": 0.5
  }'
```

### Batch Import (Query Parameters)
```http
POST /import/mobygames/batch-import
```

**Query Parameters:**
- `mobygames_ids`: List of MobyGames IDs
- `price` (optional): Product price (default: 29.99)
- `stock_quantity` (optional): Stock quantity (default: 10)
- `delay` (optional): Delay between imports in seconds (default: 1.0)

**Example:**
```bash
curl -X POST "http://localhost:8000/import/mobygames/batch-import?mobygames_ids=1&mobygames_ids=2&mobygames_ids=3&price=29.99"
```

## 🔍 Search & Import

### Search and Import Games
```http
POST /import/mobygames/search
```

**Request Body:**
```json
{
  "search_query": "mario",
  "limit": 5,
  "price": 19.99,
  "stock_quantity": 12,
  "category": "Retro Games"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/import/mobygames/search \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "sonic",
    "limit": 3,
    "price": 22.99,
    "stock_quantity": 10
  }'
```

## 📊 Status & History

### Check Import Status
```http
GET /import/mobygames/{mobygames_id}/status
```

**Example:**
```bash
curl http://localhost:8000/import/mobygames/1/status
```

### Get Import History
```http
GET /import/mobygames/history?limit=50
```

**Query Parameters:**
- `limit` (optional): Number of recent imports to return (default: 50, max: 100)

**Example:**
```bash
curl "http://localhost:8000/import/mobygames/history?limit=10"
```

### Get Import Statistics
```http
GET /import/mobygames/stats
```

**Example:**
```bash
curl http://localhost:8000/import/mobygames/stats
```

## 🗑️ Management

### Remove Imported Game
```http
DELETE /import/mobygames/{mobygames_id}
```

**Example:**
```bash
curl -X DELETE http://localhost:8000/import/mobygames/1
```

## 📋 Response Formats

### Single Import Response
```json
{
  "success": true,
  "message": "Game 'The X-Files Game' imported successfully!",
  "mobygames_id": 1,
  "game_title": "The X-Files Game",
  "woocommerce_product_id": 123,
  "price": 39.99,
  "stock_quantity": 15,
  "category": "Retro Games",
  "moby_score": 7.1,
  "platforms": ["Windows", "PlayStation", "Macintosh"],
  "genres": ["Adventure", "1st-person", "Live action"],
  "woocommerce_url": "https://retro-replay.com/product/the-x-files-game",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Bulk Import Response
```json
{
  "success": true,
  "message": "Bulk import completed: 3 successful, 0 failed",
  "summary": {
    "total": 3,
    "successful": 3,
    "failed": 0,
    "success_rate": "100.0%"
  },
  "results": [
    {
      "success": true,
      "mobygames_id": 1,
      "game_title": "The X-Files Game",
      "woocommerce_product_id": 123,
      "price": 29.99,
      "stock_quantity": 10,
      "category": "Retro Games",
      "moby_score": 7.1,
      "platforms": ["Windows", "PlayStation"],
      "genres": ["Adventure"],
      "timestamp": "2024-01-15T10:30:00"
    }
  ],
  "timestamp": "2024-01-15T10:35:00"
}
```

### Import Status Response
```json
{
  "success": true,
  "imported": true,
  "mobygames_id": 1,
  "game_title": "The X-Files Game",
  "woocommerce_product_id": 123,
  "woocommerce_url": "https://retro-replay.com/product/the-x-files-game",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Import History Response
```json
{
  "success": true,
  "total_imported": 25,
  "games": [
    {
      "woocommerce_product_id": 123,
      "mobygames_id": "1",
      "title": "The X-Files Game",
      "price": "39.99",
      "stock_quantity": 15,
      "date_created": "2024-01-15T10:30:00",
      "woocommerce_url": "https://retro-replay.com/product/the-x-files-game"
    }
  ],
  "timestamp": "2024-01-15T10:30:00"
}
```

### Import Statistics Response
```json
{
  "success": true,
  "stats": {
    "total_imported": 25,
    "average_price": 29.45,
    "total_stock_value": 250,
    "recent_imports": 25
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🧪 Testing

### Run the Test Script
```bash
python test_import.py
```

This will test all import endpoints and functionality.

### Manual Testing Examples

**Test single import:**
```bash
curl -X POST "http://localhost:8000/import/mobygames/quick-import?mobygames_id=1&price=39.99"
```

**Test bulk import:**
```bash
curl -X POST http://localhost:8000/import/mobygames/bulk \
  -H "Content-Type: application/json" \
  -d '{"mobygames_ids": [1, 2, 3], "price": 29.99}'
```

**Test search and import:**
```bash
curl -X POST http://localhost:8000/import/mobygames/search \
  -H "Content-Type: application/json" \
  -d '{"search_query": "mario", "limit": 3, "price": 19.99}'
```

## 🔧 Configuration

### Environment Variables
Make sure these are set in your `.env` file:

```env
# MobyGames API
MOBYGAMES_API_KEY=your_mobygames_api_key

# WooCommerce API
WOOCOMMERCE_URL=https://retro-replay.com
WOOCOMMERCE_CONSUMER_KEY=ck_6235d3701bcf965a1e54cb5e5b517fe38e639ff2
WOOCOMMERCE_CONSUMER_SECRET=cs_3987474b7cfcd51ff7f9abecaa86cbbb7080fea8
```

## 🚨 Error Handling

### Common Error Responses

**Game not found:**
```json
{
  "success": false,
  "error": "Game not found on MobyGames",
  "timestamp": "2024-01-15T10:30:00"
}
```

**WooCommerce connection failed:**
```json
{
  "success": false,
  "error": "WooCommerce API connection failed",
  "timestamp": "2024-01-15T10:30:00"
}
```

**Validation error:**
```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "ensure this value is greater than or equal to 0",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

## 📈 Best Practices

1. **Rate Limiting**: Use delays between bulk imports to avoid overwhelming APIs
2. **Error Handling**: Always check response status and handle errors gracefully
3. **Batch Sizes**: Keep bulk imports to reasonable sizes (10-20 games max)
4. **Monitoring**: Use status and history endpoints to track imports
5. **Testing**: Test with small batches before large imports

## 🔍 Troubleshooting

### Common Issues:

1. **Import Fails**: Check MobyGames API key and WooCommerce credentials
2. **Slow Imports**: Increase delay between imports
3. **Missing Data**: Some games may have incomplete data on MobyGames
4. **Duplicate Products**: Check if game is already imported before importing

### Debug Mode:

Enable detailed logging by setting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

**Happy Importing! 🎮**
