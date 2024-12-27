from contextlib import contextmanager
from database.main import MongoDB
from typing import Generator


@contextmanager
def get_db_connection(
    connection_string: str = "mongodb://localhost:27017/",
) -> Generator[MongoDB, None, None]:
    db = MongoDB(connection_string)
    try:
        yield db
    finally:
        db.client.close()
