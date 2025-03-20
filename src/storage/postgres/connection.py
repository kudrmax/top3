from sqlalchemy import create_engine

from src.settings.settings import settings

engine = create_engine(
    settings.db.url,
    future=True,
    echo=False
)
