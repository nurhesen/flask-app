from app.models.post import Post
from app.schemas.post import PostCreate, PostOut
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.utils.caching import cache_get, cache_set
from typing import List


def create_post(user, post: PostCreate) -> int:
    """
    Create a post for the given user.
    """
    db: Session = next(get_db())
    new_post = Post(text=post.text, user_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # Invalidate cache if necessary
    cache_set(user.id, None)
    return new_post.id


def get_posts(user) -> List[PostOut]:
    """
    Retrieve posts for the given user.
    Uses caching to reduce database calls.
    """
    # Check cache first
    cached = cache_get(user.id)
    if cached is not None:
        return cached
    
    db: Session = next(get_db())
    posts = db.query(Post).filter(Post.user_id == user.id).all()
    posts_data = [PostOut.from_orm(post) for post in posts]
    # Cache the results for 5 minutes (300 seconds)
    cache_set(user.id, posts_data, ttl=300)
    return posts_data


def delete_post(user, post_id: int) -> bool:
    """
    Delete a post for the given user.
    """
    db: Session = next(get_db())
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user.id).first()
    if not post:
        return False
    db.delete(post)
    db.commit()
    # Invalidate cache if necessary
    cache_set(user.id, None)
    return True
