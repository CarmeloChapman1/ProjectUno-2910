from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, index=True)
  image_url = Column(String)
  is_admin = Column(Boolean)

class Post(Base): 
  __tablename__ = 'posts'
  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  title = Column(String)
  post_text = Column(String)
  likes = Column(Integer)


