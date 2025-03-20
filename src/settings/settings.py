import os

from dotenv import load_dotenv

from src.settings.postgres_helper import PostgresConnection

load_dotenv()


class Postgres:

    def __init__(self):
        self.postgres_connection = PostgresConnection()

    @property
    def url(self):
        return self.postgres_connection.get_url()


class Telegram:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")

    @property
    def token(self):
        return self.BOT_TOKEN


class Settings:
    db = Postgres()
    bot = Telegram()


settings = Settings()
