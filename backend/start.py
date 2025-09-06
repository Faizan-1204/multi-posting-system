#!/usr/bin/env python3
"""
Railway startup script for Multi-Platform Posting System
"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting Multi-Platform Posting System on port {port}")
    print("📡 Backend API will be available at the Railway URL")
    print("✅ Mock login credentials: any email/password combination")
    
    uvicorn.run(
        "simple_main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
