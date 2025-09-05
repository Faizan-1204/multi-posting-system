'use client';

import { useState } from 'react';
import { postsService, Post } from '@/lib/posts';
import { Calendar, Clock, CheckCircle, XCircle, AlertCircle, Trash2 } from 'lucide-react';

interface PostsListProps {
  posts: Post[];
  onPostUpdated: () => void;
}

export default function PostsList({ posts, onPostUpdated }: PostsListProps) {
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const handleDeletePost = async (postId: number) => {
    if (confirm('Are you sure you want to delete this post?')) {
      setDeletingId(postId);
      try {
        await postsService.deletePost(postId);
        onPostUpdated();
      } catch (error) {
        console.error('Failed to delete post:', error);
      } finally {
        setDeletingId(null);
      }
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'published':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'failed':
        return <XCircle className="w-4 h-4 text-red-500" />;
      case 'publishing':
        return <Clock className="w-4 h-4 text-blue-500" />;
      default:
        return <AlertCircle className="w-4 h-4 text-yellow-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published':
        return 'bg-green-100 text-green-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'publishing':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-yellow-100 text-yellow-800';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  if (posts.length === 0) {
    return (
      <div className="bg-white shadow rounded-lg p-6 text-center">
        <p className="text-gray-500">No posts yet. Create your first post above!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-gray-900">Your Posts</h2>
      
      <div className="space-y-4">
        {posts.map((post) => (
          <div key={post.id} className="bg-white shadow rounded-lg p-6">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  {getStatusIcon(post.status)}
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(post.status)}`}>
                    {post.status}
                  </span>
                </div>
                
                <p className="text-gray-900 mb-3">{post.text}</p>
                
                {/* Media Files */}
                {post.media && post.media.length > 0 && (
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mb-3">
                    {post.media.map((media) => (
                      <div key={media.id} className="aspect-square bg-gray-100 rounded-lg flex items-center justify-center">
                        {media.type === 'image' ? (
                          <img
                            src={media.url || '#'}
                            alt="Post media"
                            className="w-full h-full object-cover rounded-lg"
                          />
                        ) : (
                          <div className="text-center">
                            <div className="text-2xl">🎥</div>
                            <div className="text-xs text-gray-500">Video</div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
                
                <div className="flex items-center space-x-4 text-sm text-gray-500">
                  <div className="flex items-center space-x-1">
                    <Calendar className="w-4 h-4" />
                    <span>Created: {formatDate(post.created_at)}</span>
                  </div>
                  {post.scheduled_at && (
                    <div className="flex items-center space-x-1">
                      <Clock className="w-4 h-4" />
                      <span>Scheduled: {formatDate(post.scheduled_at)}</span>
                    </div>
                  )}
                </div>
              </div>
              
              <button
                onClick={() => handleDeletePost(post.id)}
                disabled={deletingId === post.id}
                className="text-red-600 hover:text-red-800 p-1 disabled:opacity-50"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
