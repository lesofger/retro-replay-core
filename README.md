# Retro Replay Core - WooCommerce Integration

A FastAPI backend for managing retro game products in WooCommerce with data from IGDB and MobyGames.

## 🎮 Features

- **WooCommerce Integration**: Create and manage products in your WordPress/WooCommerce store
- **Game Data Sources**: Search and fetch game information from IGDB and MobyGames APIs
- **Product Management**: Full CRUD operations for WooCommerce products
- **Bulk Operations**: Create multiple game products at once
- **Mock Data**: Pre-loaded with 15 classic retro games for testing

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file with your API credentials:

```env
# IGDB API (optional - for game search)
IGDB_CLIENT_ID=your_igdb_client_id
IGDB_CLIENT_SECRET=your_igdb_client_secret

# MobyGames API (optional - for game search)
MOBYGAMES_API_KEY=your_mobygames_api_key

# WooCommerce API (required)
WOOCOMMERCE_URL=https://retro-replay.com
WOOCOMMERCE_CONSUMER_KEY=ck_6235d3701bcf965a1e54cb5e5b517fe38e639ff2
WOOCOMMERCE_CONSUMER_SECRET=cs_3987474b7cfcd51ff7f9abecaa86cbbb7080fea8
```

### 3. Start the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### WooCommerce Product Management

- `POST /woocommerce/products/game` - Create product from game data
- `POST /woocommerce/bulk-create-games` - Create multiple game products
- `GET /woocommerce/products` - List all products
- `GET /woocommerce/products/{id}` - Get specific product
- `PUT /woocommerce/products/{id}` - Update product
- `DELETE /woocommerce/products/{id}` - Delete product
- `POST /woocommerce/test-connection` - Test WooCommerce connection

### Game Data Search

- `GET /games/search/igdb` - Search games on IGDB
- `GET /games/search/mobygames` - Search games on MobyGames
- `GET /games/platforms` - Get available platforms
- `GET /games/genres` - Get available genres
- `GET /games/igdb/{id}` - Get specific game from IGDB
- `GET /games/mobygames/{id}` - Get specific game from MobyGames

## 🧪 Testing

### Run the Test Script

```bash
python test_woocommerce.py
```

This will test the WooCommerce integration with mock data.

### Manual Testing

```bash
# Test connection
curl -X POST http://localhost:8000/woocommerce/test-connection

# Create a game product
curl -X POST http://localhost:8000/woocommerce/products/game \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Super Mario Bros.",
    "platforms": ["NES"],
    "genres": ["Platform"],
    "price": 19.99
  }'
```

## 📖 API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🎮 Mock Game Data

The system includes 15 classic retro games for testing:

- Super Mario Bros. (NES) - $19.99
- The Legend of Zelda (NES) - $24.99
- Sonic the Hedgehog (Genesis) - $22.99
- Street Fighter II (Arcade/SNES/Genesis) - $29.99
- Final Fantasy VII (PlayStation) - $39.99
- And 10 more classic games...

## 🏗️ Project Structure

```
retro-replay-core/
├── api/
│   ├── game_routes.py          # Game search endpoints
│   └── woocommerce_routes.py   # WooCommerce product endpoints
├── models/
│   ├── external_api_models.py  # IGDB/MobyGames models
│   └── woocommerce_models.py   # WooCommerce product models
├── services/
│   ├── igdb_service.py         # IGDB API integration
│   ├── mobygames_service.py    # MobyGames API integration
│   └── woocommerce_service.py  # WooCommerce API integration
├── data/
│   └── mock_games.py           # Mock game data
├── config.py                   # Configuration settings
├── main.py                     # FastAPI application
├── test_woocommerce.py         # Test script
└── requirements.txt            # Python dependencies
```

## 🔧 Configuration

All configuration is handled through environment variables or defaults in `config.py`:

- **WooCommerce**: Your store URL and API credentials
- **IGDB**: Client ID and secret for game data
- **MobyGames**: API key for additional game data
- **Server**: Host and port settings

## 🚨 Troubleshooting

### Common Issues:

1. **WooCommerce Connection Failed**: Check your store URL and API credentials
2. **Authentication Error**: Verify consumer key and secret are correct
3. **Product Creation Failed**: Ensure required fields are provided
4. **CORS Issues**: Check CORS configuration in main.py

### Debug Mode:

Add logging to see detailed API requests:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Review the test script output
3. Check your WooCommerce store admin panel
4. Verify API credentials in WooCommerce settings

---

**Happy Gaming! 🎮**