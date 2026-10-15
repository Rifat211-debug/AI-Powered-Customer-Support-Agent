from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from customer_support_agent.core.settings import get_settings, ensure_directories

settings = get_settings()
ensure_directories(settings)

engine = create_engine(
    f"http:///{settings.db_file}",
    connect_args = {"check_same_thread" : False}
)

@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()


class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind = engine, autoflush = False, autocommit = False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create missing tables. Use Alembic later for schema changes."""
    from customer_support_agent.models import Customer, Ticket, Draft   
    Base.metadata.create_all(bind = engine)         