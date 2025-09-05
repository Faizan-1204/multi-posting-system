'use client';

import { useState } from 'react';
import { socialAccountsService, SocialAccount } from '@/lib/social-accounts';
import { Facebook, Instagram, Music, Trash2 } from 'lucide-react';

interface LinkSocialAccountsProps {
  socialAccounts: SocialAccount[];
  onAccountLinked: () => void;
}

export default function LinkSocialAccounts({ socialAccounts, onAccountLinked }: LinkSocialAccountsProps) {
  const [isLinking, setIsLinking] = useState<string | null>(null);

  const handleLinkAccount = async (provider: string) => {
    setIsLinking(provider);
    
    try {
      const redirectUri = `${window.location.origin}/auth/callback`;
      let authUrl: string;
      
      if (provider === 'facebook') {
        const response = await socialAccountsService.getFacebookAuthUrl(redirectUri);
        authUrl = response.auth_url;
      } else if (provider === 'tiktok') {
        const response = await socialAccountsService.getTikTokAuthUrl(redirectUri);
        authUrl = response.auth_url;
      } else {
        throw new Error('Unsupported provider');
      }
      
      // Open OAuth flow in new window
      const popup = window.open(
        authUrl,
        'oauth',
        'width=600,height=600,scrollbars=yes,resizable=yes'
      );
      
      // Listen for the popup to close
      const checkClosed = setInterval(() => {
        if (popup?.closed) {
          clearInterval(checkClosed);
          setIsLinking(null);
          onAccountLinked();
        }
      }, 1000);
      
    } catch (error) {
      console.error('Failed to initiate OAuth:', error);
      setIsLinking(null);
    }
  };

  const handleDeleteAccount = async (accountId: number) => {
    if (confirm('Are you sure you want to disconnect this account?')) {
      try {
        await socialAccountsService.deleteAccount(accountId);
        onAccountLinked();
      } catch (error) {
        console.error('Failed to delete account:', error);
      }
    }
  };

  const getProviderIcon = (provider: string) => {
    switch (provider) {
      case 'facebook':
        return <Facebook className="w-5 h-5 text-blue-600" />;
      case 'instagram':
        return <Instagram className="w-5 h-5 text-pink-600" />;
      case 'tiktok':
        return <Music className="w-5 h-5 text-black" />;
      default:
        return <div className="w-5 h-5 bg-gray-400 rounded" />;
    }
  };

  const getProviderName = (provider: string) => {
    switch (provider) {
      case 'facebook':
        return 'Facebook';
      case 'instagram':
        return 'Instagram';
      case 'tiktok':
        return 'TikTok';
      default:
        return provider;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Social Accounts</h2>
        <p className="mt-1 text-sm text-gray-600">
          Connect your social media accounts to start posting across platforms.
        </p>
      </div>

      {/* Available Providers */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {['facebook', 'instagram', 'tiktok'].map((provider) => {
          const isConnected = socialAccounts.some(account => account.provider === provider);
          const isLinkingThis = isLinking === provider;
          
          return (
            <div
              key={provider}
              className={`relative bg-white p-6 rounded-lg border-2 ${
                isConnected ? 'border-green-200 bg-green-50' : 'border-gray-200'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {getProviderIcon(provider)}
                  <div>
                    <h3 className="text-lg font-medium text-gray-900">
                      {getProviderName(provider)}
                    </h3>
                    <p className="text-sm text-gray-500">
                      {isConnected ? 'Connected' : 'Not connected'}
                    </p>
                  </div>
                </div>
                
                <div className="flex space-x-2">
                  {isConnected ? (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Connected
                    </span>
                  ) : (
                    <button
                      onClick={() => handleLinkAccount(provider)}
                      disabled={isLinkingThis}
                      className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isLinkingThis ? 'Connecting...' : 'Connect'}
                    </button>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Connected Accounts List */}
      {socialAccounts.length > 0 && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Connected Accounts</h3>
          </div>
          <div className="divide-y divide-gray-200">
            {socialAccounts.map((account) => (
              <div key={account.id} className="px-6 py-4 flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {getProviderIcon(account.provider)}
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {getProviderName(account.provider)}
                    </p>
                    <p className="text-sm text-gray-500">
                      ID: {account.provider_account_id}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => handleDeleteAccount(account.id)}
                  className="text-red-600 hover:text-red-800 p-1"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
