from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ScrapyProjectItem(Base):
    __tablename__ = 'flats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False)
    image = Column(String, unique=True)
