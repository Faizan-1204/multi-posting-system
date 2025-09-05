from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import SocialAccount, User
from schemas import SocialAccountResponse
from auth import get_current_active_user

router = APIRouter(prefix="/social-accounts", tags=["social-accounts"])

@router.get("/", response_model=List[SocialAccountResponse])
def get_social_accounts(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all social accounts for the current user."""
    accounts = db.query(SocialAccount).filter(SocialAccount.user_id == current_user.id).all()
    return accounts

@router.get("/facebook/auth-url")
def get_facebook_auth_url(
    redirect_uri: str = Query(..., description="Redirect URI for OAuth callback"),
    current_user: User = Depends(get_current_active_user)
):
    """Get Facebook OAuth authorization URL."""
    from config import FACEBOOK_APP_ID
    from datetime import datetime
    state = f"user_{current_user.id}_{datetime.utcnow().timestamp()}"
    auth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={FACEBOOK_APP_ID}&redirect_uri={redirect_uri}&state={state}&response_type=code&scope=pages_manage_posts,pages_read_engagement,instagram_basic,instagram_content_publish"
    return {"auth_url": auth_url, "state": state}

@router.get("/tiktok/auth-url")
def get_tiktok_auth_url(
    redirect_uri: str = Query(..., description="Redirect URI for OAuth callback"),
    current_user: User = Depends(get_current_active_user)
):
    """Get TikTok OAuth authorization URL."""
    from config import TIKTOK_APP_KEY
    from datetime import datetime
    state = f"user_{current_user.id}_{datetime.utcnow().timestamp()}"
    auth_url = f"https://www.tiktok.com/v2/auth/authorize/?client_key={TIKTOK_APP_KEY}&response_type=code&scope=user.info.basic,video.publish&redirect_uri={redirect_uri}&state={state}"
    return {"auth_url": auth_url, "state": state}
