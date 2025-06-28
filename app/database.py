from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://hine_user:9U7vaSaGEg4wpRABuRh2walWtIIh4JNC@dpg-d16fqtodl3ps739b4akg-a.oregon-postgres.render.com/hine"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 