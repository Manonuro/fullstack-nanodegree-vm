import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
        'id' : self.id,
        'name' : self.name,
        'user_id' : self.user_id
            }


class Item(Base):
    __tablename__ = 'item'
    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer, ForeignKey('category.id'))
    description = Column(String(250))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
        'cat_id' : self.cat_id,
        'description' : self.description,
        'id' : self.id,
        'title' : self.title,
            }


engine = create_engine('sqlite:///itemCatalogwithusers.db', connect_args={'check_same_thread': False})


Base.metadata.create_all(engine)
