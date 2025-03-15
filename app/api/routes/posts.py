from fastapi import APIRouter, HTTPException, status, Depends, Request
from app.schemas import post as post_schema
from app.services import post_service
from app.api.dependencies import get_current_user
from app.utils.validation import validate_payload_size

router = APIRouter()


@router.post("/add")
async def add_post(request: Request, post: post_schema.PostCreate, current_user=Depends(get_current_user)):
    await validate_payload_size(request, max_size=1 * 1024 * 1024)
    post_id = post_service.create_post(current_user, post)
    return {"postID": post_id}


@router.get("/get")
def get_posts(current_user=Depends(get_current_user)):
    posts = post_service.get_posts(current_user)
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return posts


@router.delete("/delete/{post_id}")
def delete_post(post_id: int, current_user=Depends(get_current_user)):
    result = post_service.delete_post(current_user, post_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post deletion failed")
    return {"detail": "Post deleted successfully"}
