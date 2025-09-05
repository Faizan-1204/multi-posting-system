'use client';

import { useState, useEffect } from 'react';
import { authService, User } from '@/lib/auth';
import { socialAccountsService, SocialAccount } from '@/lib/social-accounts';
import { postsService, Post } from '@/lib/posts';
import LinkSocialAccounts from '@/components/LinkSocialAccounts';
import CreatePost from '@/components/CreatePost';
import PostsList from '@/components/PostsList';
import LoginForm from '@/components/LoginForm';

export default function Home() {
  const [user, setUser] = useState<User | null>(null);
  const [socialAccounts, setSocialAccounts] = useState<SocialAccount[]>([]);
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'posts' | 'accounts'>('posts');

  useEffect(() => {
    const initApp = async () => {
      if (authService.isAuthenticated()) {
        try {
          const currentUser = await authService.getCurrentUser();
          setUser(currentUser);
          
          const accounts = await socialAccountsService.getAccounts();
          setSocialAccounts(accounts);
          
          const userPosts = await postsService.getPosts();
          setPosts(userPosts);
        } catch (error) {
          console.error('Failed to load user data:', error);
          authService.logout();
        }
      }
      setLoading(false);
    };

    initApp();
  }, []);

  const handleLogin = async (email: string, password: string) => {
    try {
      await authService.login({ email, password });
      const currentUser = await authService.getCurrentUser();
      setUser(currentUser);
      
      const accounts = await socialAccountsService.getAccounts();
      setSocialAccounts(accounts);
      
      const userPosts = await postsService.getPosts();
      setPosts(userPosts);
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const handleLogout = () => {
    authService.logout();
    setUser(null);
    setSocialAccounts([]);
    setPosts([]);
  };

  const handleAccountLinked = async () => {
    const accounts = await socialAccountsService.getAccounts();
    setSocialAccounts(accounts);
  };

  const handlePostCreated = async () => {
    const userPosts = await postsService.getPosts();
    setPosts(userPosts);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!user) {
    return <LoginForm onLogin={handleLogin} />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                Multi-Platform Posting System
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">Welcome, {user.name}</span>
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('posts')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'posts'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Posts
            </button>
            <button
              onClick={() => setActiveTab('accounts')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'accounts'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Social Accounts
            </button>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'posts' && (
          <div className="space-y-6">
            <CreatePost onPostCreated={handlePostCreated} socialAccounts={socialAccounts} />
            <PostsList posts={posts} onPostUpdated={handlePostCreated} />
          </div>
        )}
        
        {activeTab === 'accounts' && (
          <LinkSocialAccounts 
            socialAccounts={socialAccounts} 
            onAccountLinked={handleAccountLinked}
          />
        )}
      </main>
    </div>
  );
}