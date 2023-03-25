from typing import Optional
from config import db_string
from models import User, Record
from sqlmodel import Field, SQLModel, create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(db_string, echo=True)
Session = sessionmaker(engine)
session = Session()

SQLModel.metadata.create_all(engine)
