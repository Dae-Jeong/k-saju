import axios, { AxiosError } from 'axios';

import { envConfig } from '@/common/constants/env-config';
import { ApiError } from './api-error';

export const apiClient = axios.create({
  baseURL: envConfig.apiBaseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error instanceof AxiosError) {
      return Promise.reject(new ApiError(error));
    }

    return Promise.reject(error);
  },
);
