from sqlalchemy import create_engine

from src.settings.settings import settings

engine = create_engine(
    settings.db.url,
    connect_args={"options": "-c timezone=Europe/Moscow"},
    future=True,
    echo=False,
)
