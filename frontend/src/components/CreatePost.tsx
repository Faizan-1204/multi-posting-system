'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { postsService, PostCreate } from '@/lib/posts';
import { SocialAccount } from '@/lib/social-accounts';
import { Upload, X, Send } from 'lucide-react';

const postSchema = z.object({
  text: z.string().min(1, 'Post text is required'),
  scheduled_at: z.string().optional(),
});

type PostFormData = z.infer<typeof postSchema>;

interface CreatePostProps {
  onPostCreated: () => void;
  socialAccounts: SocialAccount[];
}

export default function CreatePost({ onPostCreated, socialAccounts }: CreatePostProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [selectedAccounts, setSelectedAccounts] = useState<number[]>([]);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<PostFormData>({
    resolver: zodResolver(postSchema),
  });

  const handleFileUpload = async (files: FileList) => {
    setIsUploading(true);
    try {
      const uploadPromises = Array.from(files).map(file => postsService.uploadMedia(file));
      await Promise.all(uploadPromises);
      setUploadedFiles(prev => [...prev, ...Array.from(files)]);
    } catch (error) {
      console.error('File upload failed:', error);
    } finally {
      setIsUploading(false);
    }
  };

  const removeFile = (index: number) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const onSubmit = async (data: PostFormData) => {
    if (socialAccounts.length === 0) {
      alert('Please connect at least one social account first.');
      return;
    }

    setIsSubmitting(true);
    try {
      const postData: PostCreate = {
        text: data.text,
        scheduled_at: data.scheduled_at || undefined,
        target_accounts: selectedAccounts.length > 0 ? selectedAccounts : socialAccounts.map(acc => acc.id),
      };

      const post = await postsService.createPost(postData);
      
      // Publish the post
      await postsService.publishPost(post.id, postData.target_accounts);
      
      reset();
      setSelectedAccounts([]);
      setUploadedFiles([]);
      onPostCreated();
    } catch (error) {
      console.error('Failed to create post:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">Create New Post</h3>
      </div>
      
      <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-6">
        {/* Post Text */}
        <div>
          <label htmlFor="text" className="block text-sm font-medium text-gray-700">
            Post Content
          </label>
          <textarea
            {...register('text')}
            rows={4}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="What's on your mind?"
          />
          {errors.text && (
            <p className="mt-1 text-sm text-red-600">{errors.text.message}</p>
          )}
        </div>

        {/* File Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Media Files
          </label>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
            <input
              type="file"
              multiple
              accept="image/*,video/*"
              onChange={(e) => e.target.files && handleFileUpload(e.target.files)}
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="cursor-pointer flex flex-col items-center"
            >
              <Upload className="w-8 h-8 text-gray-400 mb-2" />
              <span className="text-sm text-gray-600">
                {isUploading ? 'Uploading...' : 'Click to upload images or videos'}
              </span>
            </label>
          </div>
          
          {/* Uploaded Files */}
          {uploadedFiles.length > 0 && (
            <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
              {uploadedFiles.map((file, index) => (
                <div key={index} className="relative group">
                  <div className="aspect-square bg-gray-100 rounded-lg flex items-center justify-center">
                    {file.type.startsWith('image/') ? (
                      <img
                        src={URL.createObjectURL(file)}
                        alt={file.name}
                        className="w-full h-full object-cover rounded-lg"
                      />
                    ) : (
                      <div className="text-center">
                        <div className="text-2xl">🎥</div>
                        <div className="text-xs text-gray-500">{file.name}</div>
                      </div>
                    )}
                  </div>
                  <button
                    type="button"
                    onClick={() => removeFile(index)}
                    className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Scheduling */}
        <div>
          <label htmlFor="scheduled_at" className="block text-sm font-medium text-gray-700">
            Schedule Post (Optional)
          </label>
          <input
            {...register('scheduled_at')}
            type="datetime-local"
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>

        {/* Target Accounts */}
        {socialAccounts.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Target Accounts
            </label>
            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={selectedAccounts.length === 0}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setSelectedAccounts([]);
                    } else {
                      setSelectedAccounts(socialAccounts.map(acc => acc.id));
                    }
                  }}
                  className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                />
                <span className="ml-2 text-sm text-gray-700">All accounts</span>
              </label>
              
              {socialAccounts.map((account) => (
                <label key={account.id} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedAccounts.includes(account.id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedAccounts(prev => [...prev, account.id]);
                      } else {
                        setSelectedAccounts(prev => prev.filter(id => id !== account.id));
                      }
                    }}
                    className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                  />
                  <span className="ml-2 text-sm text-gray-700 capitalize">
                    {account.provider} ({account.provider_account_id})
                  </span>
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSubmitting || socialAccounts.length === 0}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-4 h-4 mr-2" />
            {isSubmitting ? 'Publishing...' : 'Publish Post'}
          </button>
        </div>
      </form>
    </div>
  );
}
