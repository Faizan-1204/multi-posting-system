# Multi-Platform Posting System

A production-grade, one-click multi-platform posting system that allows users to compose posts and publish them simultaneously across Facebook, Instagram, and TikTok.

## 🚀 Features

### Backend (FastAPI)
- **User Authentication**: JWT-based authentication with password hashing
- **OAuth Integration**: Facebook Pages, Instagram Business, and TikTok account linking
- **Post Management**: CRUD operations for posts with media support
- **AWS S3 Integration**: Secure media file storage and delivery
- **Background Processing**: Celery workers for asynchronous publishing
- **Database**: PostgreSQL with Alembic migrations
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

### Frontend (Next.js)
- **Modern UI**: Responsive design with Tailwind CSS
- **Social Account Management**: Connect and manage multiple platforms
- **Post Composer**: Rich text editor with media upload
- **Real-time Status**: Track publishing progress and errors
- **Authentication**: Secure login and registration

### Supported Platforms
- **Facebook Pages**: Text posts with images and videos
- **Instagram Business**: Photos and videos with captions
- **TikTok**: Video content with descriptions

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Background    │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   Workers       │
│   Port: 3000    │    │   Port: 8000    │    │   (Celery)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   OAuth         │    │   PostgreSQL    │    │   Redis         │
│   Providers     │    │   Database      │    │   Message       │
│   (Meta/TikTok) │    │                 │    │   Broker        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   AWS S3        │
                       │   Media Storage │
                       └─────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Celery** - Background task processing
- **Redis** - Message broker and caching
- **AWS S3** - Media storage
- **JWT** - Authentication tokens
- **OAuth 2.0** - Social platform integration

### Frontend
- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Hook Form** - Form management
- **Zod** - Schema validation
- **Axios** - HTTP client

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL 12+
- Redis
- AWS S3 bucket
- Social media developer accounts (Facebook, TikTok)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd multi-platform-posting-system
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the API server
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local with your API URL

# Start the development server
npm run dev
```

### 4. Start Background Workers
```bash
# In a separate terminal
cd backend
celery -A celery_app worker --loglevel=info

# In another terminal for scheduled tasks
cd backend
celery -A celery_app beat --loglevel=info
```

### 5. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost/multipost_db
SECRET_KEY=your-secret-key-here
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-s3-bucket-name
REDIS_URL=redis://localhost:6379
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
TIKTOK_APP_KEY=your-tiktok-app-key
TIKTOK_APP_SECRET=your-tiktok-app-secret
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📱 Usage

1. **Register/Login**: Create an account or sign in
2. **Connect Accounts**: Link your Facebook Pages, Instagram Business, and TikTok accounts
3. **Create Posts**: Compose text posts and upload media
4. **Publish**: Select target platforms and publish simultaneously
5. **Monitor**: Track publishing status and view logs

## 🔒 Security Features

- JWT-based authentication
- Encrypted token storage
- HTTPS enforcement
- Input validation and sanitization
- Rate limiting
- CORS configuration
- Secure file uploads

## 📊 Monitoring & Logging

- Comprehensive logging system
- Error tracking and reporting
- Publishing status monitoring
- Performance metrics
- Health check endpoints

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Cloud Deployment
- **Backend**: Deploy to AWS ECS, Google Cloud Run, or DigitalOcean App Platform
- **Frontend**: Deploy to Vercel, Netlify, or AWS Amplify
- **Database**: Use managed PostgreSQL (AWS RDS, Google Cloud SQL)
- **Redis**: Use managed Redis (AWS ElastiCache, Google Cloud Memorystore)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API docs at `/docs`

## 🔮 Roadmap

- [ ] Video processing and optimization
- [ ] Post scheduling and automation
- [ ] Analytics and insights
- [ ] Team collaboration features
- [ ] Mobile app
- [ ] Additional social platforms (Twitter, LinkedIn, YouTube)
- [ ] Content templates and bulk uploads
- [ ] A/B testing for posts
