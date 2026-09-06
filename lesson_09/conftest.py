import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://postgres:123@localhost:5432/QA"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Свежая сессия SQLAlchemy для каждого теста."""
    session = Session()
    yield session
    session.close()