from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Mock User model for testing
class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True

# Mock database
users_db = {
    "test@example.com": User(id=1, name="Test User", email="test@example.com", is_active=True),
    "admin@example.com": User(id=2, name="Admin User", email="admin@example.com", is_active=True),
}

app = FastAPI(title="Multi-Platform Posting System", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Multi-Platform Posting System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/auth/login")
async def login(email: str = Form(...), password: str = Form(...)):
    """Simple mock login endpoint for testing"""
    # Simple mock login - accepts any email/password combination
    if email in users_db:
        user = users_db[email]
    else:
        # Create a new user for any email
        user = User(id=len(users_db) + 1, name=email.split('@')[0], email=email, is_active=True)
        users_db[email] = user
    
    return {
        "access_token": f"mock_token_for_{email}",
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }

@app.post("/auth/register")
async def register(email: str = Form(...), password: str = Form(...), name: str = Form(...)):
    """Simple mock register endpoint for testing"""
    if email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(id=len(users_db) + 1, name=name, email=email, is_active=True)
    users_db[email] = user
    
    return {
        "access_token": f"mock_token_for_{email}",
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }

@app.get("/auth/me")
async def get_current_user():
    """Mock endpoint to get current user"""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com"
    }

if __name__ == "__main__":
    print("🚀 Starting Multi-Platform Posting System Backend...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🔗 API Documentation: http://localhost:8000/docs")
    print("✅ Mock login credentials: any email/password combination")
    uvicorn.run("simple_main:app", host="0.0.0.0", port=8000, reload=True)