from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Social Account schemas
class SocialAccountBase(BaseModel):
    provider: str
    provider_account_id: str

class SocialAccountCreate(SocialAccountBase):
    access_token: str
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None
    meta: Optional[dict] = None

class SocialAccountResponse(SocialAccountBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Post schemas
class PostMediaBase(BaseModel):
    s3_key: str
    type: str
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None

class PostMediaCreate(PostMediaBase):
    pass

class PostMediaResponse(PostMediaBase):
    id: int
    post_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    text: Optional[str] = None
    scheduled_at: Optional[datetime] = None

class PostCreate(PostBase):
    media: Optional[List[PostMediaCreate]] = None
    target_accounts: Optional[List[int]] = None  # List of social_account_ids

class PostResponse(PostBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    media: List[PostMediaResponse] = []
    
    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
    text: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[str] = None

# Post Target schemas
class PostTargetBase(BaseModel):
    social_account_id: int

class PostTargetCreate(PostTargetBase):
    pass

class PostTargetResponse(PostTargetBase):
    id: int
    post_id: int
    platform_status: str
    platform_post_id: Optional[str] = None
    last_error: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Log schemas
class LogResponse(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    level: str
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# File upload schemas
class FileUploadResponse(BaseModel):
    filename: str
    s3_key: str
    url: str
    size: int
    content_type: str
