from sqlalchemy import create_engine # for the connection pool = the taxi waiter.
from sqlalchemy.orm import sessionmaker # make a session which is the identy that enter your web server
from dotenv import load_dotenv # protect my database credentials
import os # get acces to the .env file

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        

