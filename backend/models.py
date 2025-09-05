from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    social_accounts = relationship("SocialAccount", back_populates="user")
    posts = relationship("Post", back_populates="user")

class SocialAccount(Base):
    __tablename__ = "social_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String(50), nullable=False)  # 'facebook', 'instagram', 'tiktok'
    provider_account_id = Column(String(255), nullable=False)
    access_token_encrypted = Column(Text, nullable=False)
    refresh_token_encrypted = Column(Text)
    token_expires_at = Column(DateTime(timezone=True))
    meta = Column(JSON)  # Store additional provider-specific data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="social_accounts")
    post_targets = relationship("PostTarget", back_populates="social_account")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    scheduled_at = Column(DateTime(timezone=True))
    status = Column(String(50), default="draft")  # 'draft', 'scheduled', 'publishing', 'published', 'failed'
    
    # Relationships
    user = relationship("User", back_populates="posts")
    media = relationship("PostMedia", back_populates="post")
    targets = relationship("PostTarget", back_populates="post")

class PostMedia(Base):
    __tablename__ = "post_media"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    s3_key = Column(String(500), nullable=False)
    type = Column(String(50), nullable=False)  # 'image', 'video'
    width = Column(Integer)
    height = Column(Integer)
    duration = Column(Integer)  # For videos, in seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    post = relationship("Post", back_populates="media")

class PostTarget(Base):
    __tablename__ = "post_targets"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    social_account_id = Column(Integer, ForeignKey("social_accounts.id"), nullable=False)
    platform_status = Column(String(50), default="pending")  # 'pending', 'publishing', 'published', 'failed'
    platform_post_id = Column(String(255))  # ID returned by the platform
    last_error = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    post = relationship("Post", back_populates="targets")
    social_account = relationship("SocialAccount", back_populates="post_targets")

class Log(Base):
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False)  # 'post', 'social_account', 'user'
    entity_id = Column(Integer, nullable=False)
    level = Column(String(20), nullable=False)  # 'info', 'warning', 'error'
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
