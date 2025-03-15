from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1024), nullable=False)  # Adjust length as needed.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
