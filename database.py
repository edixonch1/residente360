from sqlalchemy import create_engine
from models import Base

engine = create_engine("sqlite:///residente360.db", echo=True)

Base.metadata.create_all(bind=engine)