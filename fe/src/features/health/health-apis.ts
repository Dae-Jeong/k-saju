import { apiClient } from '@/common/apis/api-client';
import type { HealthStatus } from './health-types';

/**
 * `/health/ready` returns its body bare (no envelope) — unlike most
 * endpoints, it is not wrapped in `{ data, message, meta }`.
 */
export const getHealth = async (): Promise<HealthStatus> => {
  const response = await apiClient.get<HealthStatus>('/health/ready');

  return response.data;
};
