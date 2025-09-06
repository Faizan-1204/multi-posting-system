# 🚀 Railway Deployment Guide

## Quick Deploy to Railway (5 minutes)

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway
```bash
railway login
```

### Step 3: Initialize Railway Project
```bash
railway init
```

### Step 4: Deploy Backend
```bash
cd backend
railway up
```

### Step 5: Deploy Frontend
```bash
cd ../frontend
railway up
```

## Alternative: Deploy via Railway Dashboard

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect the backend and frontend
6. Deploy!

## Environment Variables (Optional)

Add these in Railway dashboard if needed:
- `PORT` (auto-set by Railway)
- `SECRET_KEY` (for production)
- `DATABASE_URL` (if using PostgreSQL)

## What You Get

- ✅ **Backend API**: FastAPI with authentication
- ✅ **Frontend**: Next.js dashboard
- ✅ **Database**: Ready for PostgreSQL
- ✅ **File Storage**: AWS S3 integration
- ✅ **Social Media**: Facebook, Instagram, TikTok APIs
- ✅ **Background Jobs**: Celery + Redis
- ✅ **Auto-scaling**: Railway handles everything

## Testing Your Deployment

1. **Backend Health**: `https://your-app.railway.app/health`
2. **API Docs**: `https://your-app.railway.app/docs`
3. **Frontend**: `https://your-frontend.railway.app`

## Mock Login Credentials

- **Email**: any email (e.g., `test@example.com`)
- **Password**: any password (e.g., `password123`)

## Next Steps After Deployment

1. **Set up real database** (PostgreSQL)
2. **Configure social media APIs** (Facebook, TikTok)
3. **Add file storage** (AWS S3)
4. **Set up monitoring** (Sentry, etc.)

---

**Ready to deploy? Run the commands above! 🚀**
