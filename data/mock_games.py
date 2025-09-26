"""
Mock game data for testing WooCommerce product creation
"""

MOCK_GAMES = [
    {
        "title": "Super Mario Bros.",
        "description": "The classic platformer that started it all! Guide Mario through the Mushroom Kingdom to rescue Princess Peach from Bowser's clutches. Features iconic levels, power-ups, and timeless gameplay that defined the platforming genre.",
        "platforms": ["Nintendo Entertainment System", "Nintendo Switch"],
        "genres": ["Platform", "Action"],
        "release_date": "1985-09-13",
        "developer": "Nintendo EAD",
        "publisher": "Nintendo",
        "price": 19.99
    },
    {
        "title": "The Legend of Zelda",
        "description": "Embark on an epic adventure as Link in this groundbreaking action-adventure game. Explore dungeons, solve puzzles, and battle monsters in the kingdom of Hyrule. A masterpiece that established the adventure game genre.",
        "platforms": ["Nintendo Entertainment System", "Nintendo Switch"],
        "genres": ["Action-Adventure", "RPG"],
        "release_date": "1986-02-21",
        "developer": "Nintendo EAD",
        "publisher": "Nintendo",
        "price": 24.99
    },
    {
        "title": "Sonic the Hedgehog",
        "description": "Speed through Green Hill Zone as the fastest hedgehog alive! This classic platformer introduced the world to Sonic's signature speed and attitude. Collect rings, defeat Dr. Robotnik, and save the animals of South Island.",
        "platforms": ["Sega Genesis", "Sega Mega Drive"],
        "genres": ["Platform", "Action"],
        "release_date": "1991-06-23",
        "developer": "Sonic Team",
        "publisher": "Sega",
        "price": 22.99
    },
    {
        "title": "Street Fighter II",
        "description": "The fighting game that revolutionized the arcade scene! Choose from 8 world warriors and battle in this legendary fighting game. Master special moves, combos, and strategies in the ultimate fighting tournament.",
        "platforms": ["Arcade", "Super Nintendo", "Sega Genesis"],
        "genres": ["Fighting", "Arcade"],
        "release_date": "1991-02-06",
        "developer": "Capcom",
        "publisher": "Capcom",
        "price": 29.99
    },
    {
        "title": "Final Fantasy VII",
        "description": "Join Cloud Strife and his allies in this epic RPG adventure. Battle the evil Shinra Corporation and the mysterious Sephiroth in a story that spans the planet. Features deep character development and strategic turn-based combat.",
        "platforms": ["PlayStation", "PC", "Nintendo Switch"],
        "genres": ["RPG", "Turn-based"],
        "release_date": "1997-01-31",
        "developer": "Square",
        "publisher": "Square",
        "price": 39.99
    },
    {
        "title": "Donkey Kong Country",
        "description": "Help Donkey Kong and Diddy Kong recover their stolen banana hoard from King K. Rool! This beautiful platformer features pre-rendered 3D graphics, catchy music, and challenging gameplay across multiple worlds.",
        "platforms": ["Super Nintendo", "Game Boy Advance"],
        "genres": ["Platform", "Action"],
        "release_date": "1994-11-21",
        "developer": "Rare",
        "publisher": "Nintendo",
        "price": 27.99
    },
    {
        "title": "Mega Man 2",
        "description": "The Blue Bomber returns in this classic action platformer! Battle through 8 robot masters, each with unique abilities. Collect their weapons and use them strategically to defeat Dr. Wily's latest scheme.",
        "platforms": ["Nintendo Entertainment System", "Nintendo Switch"],
        "genres": ["Action", "Platform"],
        "release_date": "1988-12-24",
        "developer": "Capcom",
        "publisher": "Capcom",
        "price": 18.99
    },
    {
        "title": "Chrono Trigger",
        "description": "Travel through time in this masterpiece RPG! Join Crono and his friends as they journey across different eras to prevent the destruction of the world. Features multiple endings and innovative battle system.",
        "platforms": ["Super Nintendo", "Nintendo DS", "PC"],
        "genres": ["RPG", "Time Travel"],
        "release_date": "1995-03-11",
        "developer": "Square",
        "publisher": "Square",
        "price": 34.99
    },
    {
        "title": "Castlevania: Symphony of the Night",
        "description": "Explore Dracula's castle as Alucard in this gothic masterpiece! This Metroidvania classic features non-linear exploration, RPG elements, and beautiful 2D graphics. A true work of art in gaming.",
        "platforms": ["PlayStation", "Sega Saturn", "Xbox 360"],
        "genres": ["Action-Adventure", "Metroidvania"],
        "release_date": "1997-03-20",
        "developer": "Konami",
        "publisher": "Konami",
        "price": 32.99
    },
    {
        "title": "Super Metroid",
        "description": "Bounty hunter Samus Aran returns in this atmospheric adventure! Explore the planet Zebes, collect power-ups, and battle the Space Pirates in this influential Metroidvania that defined the genre.",
        "platforms": ["Super Nintendo", "Nintendo Switch"],
        "genres": ["Action-Adventure", "Metroidvania"],
        "release_date": "1994-03-19",
        "developer": "Nintendo R&D1",
        "publisher": "Nintendo",
        "price": 28.99
    },
    {
        "title": "Pac-Man",
        "description": "The iconic arcade classic that needs no introduction! Guide Pac-Man through mazes, eat dots, avoid ghosts, and collect power pellets. Simple yet addictive gameplay that became a cultural phenomenon.",
        "platforms": ["Arcade", "Atari 2600", "NES"],
        "genres": ["Arcade", "Maze"],
        "release_date": "1980-05-22",
        "developer": "Namco",
        "publisher": "Namco",
        "price": 12.99
    },
    {
        "title": "Tetris",
        "description": "The ultimate puzzle game that's easy to learn but hard to master! Arrange falling blocks to create complete lines and clear them from the screen. Simple mechanics with infinite replayability.",
        "platforms": ["Game Boy", "NES", "Arcade"],
        "genres": ["Puzzle", "Arcade"],
        "release_date": "1984-06-06",
        "developer": "Alexey Pajitnov",
        "publisher": "Nintendo",
        "price": 14.99
    },
    {
        "title": "Metal Gear Solid",
        "description": "Stealth action at its finest! Play as Solid Snake in this cinematic masterpiece that revolutionized the stealth genre. Infiltrate Shadow Moses Island and stop a nuclear threat in this story-driven adventure.",
        "platforms": ["PlayStation", "PC"],
        "genres": ["Stealth", "Action"],
        "release_date": "1998-09-03",
        "developer": "Konami",
        "publisher": "Konami",
        "price": 36.99
    },
    {
        "title": "Resident Evil 2",
        "description": "Survival horror perfection! Play as Leon Kennedy or Claire Redfield as they navigate the zombie-infested Raccoon City Police Department. Atmospheric horror with limited resources and strategic gameplay.",
        "platforms": ["PlayStation", "Nintendo 64", "Dreamcast"],
        "genres": ["Survival Horror", "Action"],
        "release_date": "1998-01-21",
        "developer": "Capcom",
        "publisher": "Capcom",
        "price": 33.99
    },
    {
        "title": "GoldenEye 007",
        "description": "The FPS that defined console multiplayer! Play as James Bond in this faithful adaptation of the classic film. Features groundbreaking multiplayer modes and innovative console FPS controls.",
        "platforms": ["Nintendo 64"],
        "genres": ["First-Person Shooter", "Action"],
        "release_date": "1997-08-25",
        "developer": "Rare",
        "publisher": "Nintendo",
        "price": 35.99
    }
]

def get_mock_games():
    """Return the list of mock games"""
    return MOCK_GAMES

def get_random_game():
    """Return a random game from the mock data"""
    import random
    return random.choice(MOCK_GAMES)

def get_games_by_platform(platform: str):
    """Return games filtered by platform"""
    return [game for game in MOCK_GAMES if platform.lower() in [p.lower() for p in game["platforms"]]]

def get_games_by_genre(genre: str):
    """Return games filtered by genre"""
    return [game for game in MOCK_GAMES if genre.lower() in [g.lower() for g in game["genres"]]]
