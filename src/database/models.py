from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image = Column(String, nullable=False)
    description = Column(String)
    tags = relationship('Tag', secondary='image_tag')
    comments = relationship('Comment', backref='image')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    images = relationship('Image', secondary='image_tag')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey('images.id'))
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


image_tag = Table(
    'image_tag',
    Base.metadata,
    Column('image_id', Integer, ForeignKey('images.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)
