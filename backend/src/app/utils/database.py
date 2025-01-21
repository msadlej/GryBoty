from contextlib import contextmanager
from typing import Generator

from database.main import MongoDB
from app.config import settings


@contextmanager
def get_db_connection(
    connection_string: str = settings.MONGO_URI,
) -> Generator[MongoDB, None, None]:
    db = MongoDB(connection_string)
    try:
        yield db
    finally:
        db.client.close()
