from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from datetime import datetime

from sqlalchemy import (VARCHAR, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, create_engine, text)

Base = declarative_base()

engine = create_engine('mysql+pymysql://syuhas:funstuff@mydb.cypnvtxsedui.us-east-1.rds.amazonaws.com:3306')




class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)      # 'nullable=false': this means that the column cannot be null or empty
    pw = Column(String(80), nullable=False)
    email = Column(String(120))
    firstname = Column(String(80))
    lastname = Column(String(80))
    phone = Column(String(80))
    linkedin = Column(String(80))
    confirmed = Column(Boolean, default=False)
    profile_link = Column(String(100))
    date_created = Column(DateTime, default=datetime.utcnow, nullable=False)


engine.execute('CREATE DATABASE IF NOT EXISTS userdb')
engine.execute('USE userdb')



Base.metadata.create_all(engine)