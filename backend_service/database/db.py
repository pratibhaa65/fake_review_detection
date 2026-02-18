from multiprocessing import process
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = process.env.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
