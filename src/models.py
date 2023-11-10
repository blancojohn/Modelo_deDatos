import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import declarative_base, relationship, backref
from eralchemy2 import render_er


Base = declarative_base()

followers_table = Table(
    "followers",
    Base.metadata, 
    Column("follower_id", Integer, ForeignKey('users.id'), nullable=False, primary_key=True),   
    Column("followed_id", Integer, ForeignKey('users.id'), nullable=False, primary_key=True)
)     
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(120), nullable=False, unique=True)
    firstname = Column(String(120), nullable=False)
    lastname = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    posts = relationship('Post', backref='user')
    comments = relationship('Comment', backref='user')

    followers = relationship(
        "User", 
        secondary= followers_table, 
        primaryjoin= (followers_table.c.follower_id == id), 
        secondaryjoin= (followers_table.c.followed_id == id),  
        backref= backref("followeds", lazy="dynamic") 
    )

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comments = relationship('Comment', backref='post')
    medias = relationship('Media', backref='post')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(255), nullable=False)
    posts_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)


class Media(Base):
    __tablename__ = 'medias'
    id = Column(Integer, primary_key=True)
    filename = Column(String(120), nullable=False)
    type = Column(String(40), nullable=False)
    posts_id = Column(Integer, ForeignKey('posts.id'), nullable=False)


    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
