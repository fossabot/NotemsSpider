from sqlalchemy import Column, Integer, String, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Progress(Base):
    __tablename__ = 'progress'
    id = Column(Integer, primary_key=True)
    stage = Column(String, nullable=False)
    dict_index = Column(Integer, default=0)
    brute_len = Column(Integer, default=1)
    brute_index = Column(Integer, default=0)


class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    content = Column(Text)
    __table_args__ = (UniqueConstraint('code', name='_code_uc'),)
