# Retro Replay Core

A FastAPI backend for managing your game library with data from IGDB and MobyGames APIs.

## Features

- 🎮 Game library management
- 🔍 Search games from IGDB and MobyGames
- 📊 Library statistics and analytics
- 🏷️ Game categorization and status tracking
- 🖼️ Cover images and metadata
- 📱 RESTful API with automatic documentation

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file and configure your API keys:

```bash
copy .env.example .env
```

Edit `.env` and add your API keys:

```env
# IGDB API Configuration
IGDB_CLIENT_ID=your_igdb_client_id
IGDB_CLIENT_SECRET=your_igdb_client_secret

# MobyGames API Configuration
MOBYGAMES_API_KEY=your_mobygames_api_key

# Database Configuration
DATABASE_URL=sqlite:///./game_library.db
```

### 3. Get API Keys

#### IGDB (Internet Game Database)
1. Go to [Twitch Developer Console](https://dev.twitch.tv/console)
2. Create a new application
3. Get your Client ID and Client Secret

#### MobyGames
1. Go to [MobyGames API](https://www.mobygames.com/info/api)
2. Request an API key
3. Add it to your `.env` file

### 4. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Games Library
- `GET /games/` - Get all games in your library
- `GET /games/{game_id}` - Get a specific game
- `POST /games/` - Add a new game to library
- `PUT /games/{game_id}` - Update a game
- `DELETE /games/{game_id}` - Remove a game

### Search & Import
- `GET /games/search/igdb?query={query}` - Search IGDB
- `GET /games/search/mobygames?query={query}` - Search MobyGames
- `POST /games/import/igdb/{igdb_id}` - Import from IGDB
- `POST /games/import/mobygames/{mobygames_id}` - Import from MobyGames

### Statistics
- `GET /games/stats/summary` - Get library statistics

## Game Status Options

- `want_to_play` - Games you want to play
- `playing` - Currently playing
- `completed` - Finished games
- `on_hold` - Paused games
- `dropped` - Games you stopped playing

## Project Structure

```
retro-replay-core/
├── api/
│   ├── __init__.py
│   └── game_routes.py      # Game API endpoints
├── database/
│   ├── __init__.py
│   ├── database.py         # Database configuration
│   └── models.py           # SQLAlchemy models
├── models/
│   ├── __init__.py
│   └── game_models.py      # Pydantic models
├── services/
│   ├── __init__.py
│   ├── igdb_service.py     # IGDB API integration
│   └── mobygames_service.py # MobyGames API integration
├── config.py               # Configuration settings
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Development

### Adding New Features

1. Create new models in `models/`
2. Add database tables in `database/models.py`
3. Implement services in `services/`
4. Create API routes in `api/`
5. Update `main.py` to include new routes

### Database Migrations

The application uses SQLAlchemy with automatic table creation. For production, consider using Alembic for database migrations.

## License

MIT License
