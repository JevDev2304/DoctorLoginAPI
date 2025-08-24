from sqlalchemy import Column, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String)
    birth_date = Column(Date)
    eliminated = Column(Boolean, default=False)
    password = Column(String) 