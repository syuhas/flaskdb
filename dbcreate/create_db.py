from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from datetime import datetime

from sqlalchemy import (VARCHAR, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, create_engine, text)

from flask import current_app as app

Base = declarative_base()


# this is how you configure the database to connect and create the tables
# engine = create_engine('mysql+pymysql://{databaseusername}:{databasepassword}@{databaseurl}:{databaseport}')

# here is an example of how you would connect to a database on an RDS instance
# engine = create_engine('mysql+pymysql://username:password@mydb.myurl.us-east-1.rds.amazonaws.com:3306')

# for ACTUAL PRODUCTION USE I have them set as environment variables here for security, they are loaded into the elastic beanstalk environment
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=app.config['SQLALCHEMY_ECHO'])

#  I reccomend doing it this way, as it is more secure and you can use the same code for local development



# this defines the table, the same way you do it in the database file
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

# here is where sqlalchemy creates the tables in the database
engine.execute('CREATE DATABASE IF NOT EXISTS userdb') # this creates the database if it does not exist
engine.execute('USE userdb') # this tells the engine to use the database we just created


# now we create the tables using Base. Base is the declarative base that we defined up top and used to define the User table

Base.metadata.create_all(engine)