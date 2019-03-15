from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime

from models.base import Base


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    args = Column(String(1024), nullable=False)

    created = Column(DateTime, nullable=False)

    def __init__(self, name: str, title: str, args: str):
        self.created = datetime.now()
        self.name = name
        self.title = title
        self.args = args
