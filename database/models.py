from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from models.game_models import Platform, GameStatus

Base = declarative_base()

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    release_date = Column(DateTime)
    platforms = Column(JSON)  # Store as JSON array
    genres = Column(JSON)  # Store as JSON array
    developers = Column(JSON)  # Store as JSON array
    publishers = Column(JSON)  # Store as JSON array
    cover_image_url = Column(String)
    rating = Column(Float)
    status = Column(Enum(GameStatus), default=GameStatus.WANT_TO_PLAY)
    notes = Column(Text)
    igdb_id = Column(Integer, unique=True, index=True)
    mobygames_id = Column(Integer, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
