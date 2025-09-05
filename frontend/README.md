# Multi-Platform Posting System - Frontend

This is the frontend application for the multi-platform posting system built with Next.js, TypeScript, and Tailwind CSS.

## Features

- **User Authentication**: Login and registration system
- **Social Account Linking**: Connect Facebook, Instagram, and TikTok accounts via OAuth
- **Post Creation**: Compose text posts with media uploads
- **Multi-Platform Publishing**: Publish posts to multiple social platforms simultaneously
- **Post Management**: View, edit, and delete posts
- **Real-time Status**: Track publishing status and errors

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on port 8000

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   Create a `.env.local` file in the frontend directory:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Project Structure

```
src/
├── app/                    # Next.js app directory
│   ├── auth/callback/     # OAuth callback page
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── CreatePost.tsx     # Post creation form
│   ├── LinkSocialAccounts.tsx # Social account management
│   ├── LoginForm.tsx      # Authentication form
│   └── PostsList.tsx      # Posts display
└── lib/                   # Utility functions
    ├── api.ts            # API client configuration
    ├── auth.ts           # Authentication service
    ├── posts.ts          # Posts service
    └── social-accounts.ts # Social accounts service
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## API Integration

The frontend communicates with the backend API through:

- **Authentication**: JWT-based authentication
- **Social Accounts**: OAuth flow for platform connections
- **Posts**: CRUD operations for posts and media
- **Publishing**: Queue posts for multi-platform publishing

## Technologies Used

- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Hook Form** - Form management
- **Zod** - Schema validation
- **Axios** - HTTP client
- **Lucide React** - Icons