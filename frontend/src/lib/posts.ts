import { api } from './api';

export interface PostMedia {
  id: number;
  post_id: number;
  s3_key: string;
  type: string;
  width?: number;
  height?: number;
  duration?: number;
  created_at: string;
}

export interface Post {
  id: number;
  user_id: number;
  text?: string;
  status: string;
  created_at: string;
  scheduled_at?: string;
  media: PostMedia[];
}

export interface PostCreate {
  text?: string;
  scheduled_at?: string;
  media?: Omit<PostMedia, 'id' | 'post_id' | 'created_at'>[];
  target_accounts?: number[];
}

export interface FileUploadResponse {
  filename: string;
  s3_key: string;
  url: string;
  size: number;
  content_type: string;
}

export const postsService = {
  async getPosts(skip = 0, limit = 100): Promise<Post[]> {
    const response = await api.get('/posts/', {
      params: { skip, limit },
    });
    return response.data;
  },

  async getPost(postId: number): Promise<Post> {
    const response = await api.get(`/posts/${postId}`);
    return response.data;
  },

  async createPost(data: PostCreate): Promise<Post> {
    const response = await api.post('/posts/', data);
    return response.data;
  },

  async updatePost(postId: number, data: Partial<PostCreate>): Promise<Post> {
    const response = await api.put(`/posts/${postId}`, data);
    return response.data;
  },

  async deletePost(postId: number): Promise<void> {
    await api.delete(`/posts/${postId}`);
  },

  async uploadMedia(file: File): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/posts/upload-media', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async publishPost(postId: number, targetAccounts?: number[]): Promise<any> {
    const response = await api.post(`/posts/${postId}/publish`, {
      target_accounts: targetAccounts,
    });
    return response.data;
  },
};
