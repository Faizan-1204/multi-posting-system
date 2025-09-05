from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Post, PostMedia, PostTarget, SocialAccount, User, Log
from schemas import PostCreate, PostResponse, PostUpdate, PostMediaResponse, FileUploadResponse
from auth import get_current_active_user

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[PostResponse])
def get_posts(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all posts for the current user."""
    posts = db.query(Post).filter(Post.user_id == current_user.id).offset(skip).limit(limit).all()
    return posts

@router.post("/", response_model=PostResponse)
def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new post."""
    # Create the post
    db_post = Post(
        user_id=current_user.id,
        text=post.text,
        scheduled_at=post.scheduled_at,
        status="draft"
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Add media if provided
    if post.media:
        for media_data in post.media:
            db_media = PostMedia(
                post_id=db_post.id,
                s3_key=media_data.s3_key,
                type=media_data.type,
                width=media_data.width,
                height=media_data.height,
                duration=media_data.duration
            )
            db.add(db_media)
    
    # Add target accounts if provided
    if post.target_accounts:
        for account_id in post.target_accounts:
            # Verify the account belongs to the user
            account = db.query(SocialAccount).filter(
                SocialAccount.id == account_id,
                SocialAccount.user_id == current_user.id
            ).first()
            
            if account:
                db_target = PostTarget(
                    post_id=db_post.id,
                    social_account_id=account_id,
                    platform_status="pending"
                )
                db.add(db_target)
    
    db.commit()
    db.refresh(db_post)
    
    return db_post

@router.post("/upload-media", response_model=FileUploadResponse)
def upload_media(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Upload media file to S3."""
    # For now, return mock data - in production, integrate with S3
    return FileUploadResponse(
        filename=file.filename,
        s3_key=f"media/{file.filename}",
        url=f"https://example.com/media/{file.filename}",
        size=1024,
        content_type=file.content_type or "application/octet-stream"
    )

@router.post("/{post_id}/publish")
def publish_post(
    post_id: int,
    target_accounts: Optional[List[int]] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Publish a post to selected social accounts."""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # If no target accounts specified, use all linked accounts
    if not target_accounts:
        target_accounts = [account.id for account in current_user.social_accounts]
    
    # Update post status
    post.status = "publishing"
    db.commit()
    
    return {
        "message": f"Post queued for publishing to {len(target_accounts)} accounts",
        "post_id": post_id,
        "target_accounts": target_accounts
    }
