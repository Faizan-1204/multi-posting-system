import requests
import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from models import SocialAccount, User
from config import (
    FACEBOOK_APP_ID, 
    FACEBOOK_APP_SECRET, 
    INSTAGRAM_APP_ID, 
    INSTAGRAM_APP_SECRET,
    TIKTOK_APP_KEY,
    TIKTOK_APP_SECRET
)
from cryptography.fernet import Fernet
import base64
import os

# Encryption key for storing tokens securely
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
cipher_suite = Fernet(ENCRYPTION_KEY)

def encrypt_token(token: str) -> str:
    """Encrypt a token for secure storage."""
    return cipher_suite.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    """Decrypt a token for use."""
    return cipher_suite.decrypt(encrypted_token.encode()).decode()

class FacebookOAuth:
    """Facebook OAuth handler."""
    
    @staticmethod
    def get_auth_url(redirect_uri: str, state: str) -> str:
        """Generate Facebook OAuth authorization URL."""
        params = {
            "client_id": FACEBOOK_APP_ID,
            "redirect_uri": redirect_uri,
            "state": state,
            "response_type": "code",
            "scope": "pages_manage_posts,pages_read_engagement,instagram_basic,instagram_content_publish"
        }
        return f"https://www.facebook.com/v18.0/dialog/oauth?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    @staticmethod
    def exchange_code_for_token(code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for access token."""
        url = "https://graph.facebook.com/v18.0/oauth/access_token"
        data = {
            "client_id": FACEBOOK_APP_ID,
            "client_secret": FACEBOOK_APP_SECRET,
            "redirect_uri": redirect_uri,
            "code": code
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def get_long_lived_token(short_lived_token: str) -> Dict[str, Any]:
        """Exchange short-lived token for long-lived token."""
        url = "https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": FACEBOOK_APP_ID,
            "client_secret": FACEBOOK_APP_SECRET,
            "fb_exchange_token": short_lived_token
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def get_user_pages(access_token: str) -> Dict[str, Any]:
        """Get user's Facebook pages."""
        url = "https://graph.facebook.com/v18.0/me/accounts"
        params = {"access_token": access_token}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def get_instagram_accounts(page_id: str, access_token: str) -> Dict[str, Any]:
        """Get Instagram Business accounts connected to a Facebook page."""
        url = f"https://graph.facebook.com/v18.0/{page_id}"
        params = {
            "fields": "instagram_business_account",
            "access_token": access_token
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

class TikTokOAuth:
    """TikTok OAuth handler."""
    
    @staticmethod
    def get_auth_url(redirect_uri: str, state: str) -> str:
        """Generate TikTok OAuth authorization URL."""
        params = {
            "client_key": TIKTOK_APP_KEY,
            "response_type": "code",
            "scope": "user.info.basic,video.publish",
            "redirect_uri": redirect_uri,
            "state": state
        }
        return f"https://www.tiktok.com/v2/auth/authorize/?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    @staticmethod
    def exchange_code_for_token(code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for access token."""
        url = "https://open-api.tiktok.com/oauth/access_token/"
        data = {
            "client_key": TIKTOK_APP_KEY,
            "client_secret": TIKTOK_APP_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()

def save_social_account(
    db: Session, 
    user_id: int, 
    provider: str, 
    provider_account_id: str, 
    access_token: str, 
    refresh_token: Optional[str] = None,
    token_expires_at: Optional[str] = None,
    meta: Optional[Dict[str, Any]] = None
) -> SocialAccount:
    """Save a social account to the database."""
    # Check if account already exists
    existing_account = db.query(SocialAccount).filter(
        SocialAccount.user_id == user_id,
        SocialAccount.provider == provider,
        SocialAccount.provider_account_id == provider_account_id
    ).first()
    
    if existing_account:
        # Update existing account
        existing_account.access_token_encrypted = encrypt_token(access_token)
        if refresh_token:
            existing_account.refresh_token_encrypted = encrypt_token(refresh_token)
        if token_expires_at:
            existing_account.token_expires_at = token_expires_at
        if meta:
            existing_account.meta = meta
        db.commit()
        db.refresh(existing_account)
        return existing_account
    else:
        # Create new account
        social_account = SocialAccount(
            user_id=user_id,
            provider=provider,
            provider_account_id=provider_account_id,
            access_token_encrypted=encrypt_token(access_token),
            refresh_token_encrypted=encrypt_token(refresh_token) if refresh_token else None,
            token_expires_at=token_expires_at,
            meta=meta
        )
        db.add(social_account)
        db.commit()
        db.refresh(social_account)
        return social_account

def get_decrypted_token(social_account: SocialAccount, token_type: str = "access") -> str:
    """Get decrypted token from social account."""
    if token_type == "access":
        return decrypt_token(social_account.access_token_encrypted)
    elif token_type == "refresh" and social_account.refresh_token_encrypted:
        return decrypt_token(social_account.refresh_token_encrypted)
    else:
        raise ValueError("Invalid token type or refresh token not available")
