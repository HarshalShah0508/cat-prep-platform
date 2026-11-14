from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    # Neon's pooled endpoint silently closes idle backend connections well under an
    # hour - pool_pre_ping alone doesn't catch a connection that dies *during* a
    # request (seen as "SSL connection has been closed unexpectedly" on rollback at
    # request teardown). Recycling connections before that happens avoids handing out
    # ones old enough to be at risk.
    pool_recycle=240,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
