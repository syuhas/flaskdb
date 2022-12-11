from datetime import datetime

from sqlalchemy import (VARCHAR, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, create_engine, text)

from flask import Blueprint, flash, redirect, url_for, current_app as app, session

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine



database = Blueprint('database', __name__)



Base = declarative_base()

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=app.config['SQLALCHEMY_ECHO'])


def connect():                                          # reconnects and loads fresh data from db, returns connection as local session
    Session = sessionmaker()                            # use to make sure no stale data
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=app.config['SQLALCHEMY_ECHO'])
    local_session = Session(bind=engine)
    try:
        with engine.connect() as connection:
            connection.execute("CREATE DATABASE IF NOT EXISTS userdb")
            connection.execute("USE userdb")
    except:
        flash('Database connection error. Please login and try again.')
        if "username" in session:
            session.pop['username']
        return redirect(url_for('views.home'))
    return local_session




class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False, unique=True)
    pw = Column(String(80), nullable=False)
    email = Column(String(120))
    firstname = Column(String(80))
    lastname = Column(String(80))
    phone = Column(String(80))
    linkedin = Column(String(80))
    confirmed = Column(Boolean, default=False)
    profile_link = Column(String(100))
    date_created = Column(DateTime, default=datetime.utcnow, nullable=False)






