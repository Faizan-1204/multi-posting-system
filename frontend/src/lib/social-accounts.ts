import { api } from './api';

export interface SocialAccount {
  id: number;
  user_id: number;
  provider: string;
  provider_account_id: string;
  created_at: string;
}

export interface AuthUrlResponse {
  auth_url: string;
  state: string;
}

export const socialAccountsService = {
  async getAccounts(): Promise<SocialAccount[]> {
    const response = await api.get('/social-accounts/');
    return response.data;
  },

  async getFacebookAuthUrl(redirectUri: string): Promise<AuthUrlResponse> {
    const response = await api.get('/social-accounts/facebook/auth-url', {
      params: { redirect_uri: redirectUri },
    });
    return response.data;
  },

  async getTikTokAuthUrl(redirectUri: string): Promise<AuthUrlResponse> {
    const response = await api.get('/social-accounts/tiktok/auth-url', {
      params: { redirect_uri: redirectUri },
    });
    return response.data;
  },

  async deleteAccount(accountId: number): Promise<void> {
    await api.delete(`/social-accounts/${accountId}`);
  },
};
