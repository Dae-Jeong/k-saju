import { useQuery, type UseQueryOptions } from '@tanstack/react-query';

import { getHealth } from './health-apis';
import { healthQueryKeys } from './health-query-keys';
import type { HealthStatus } from './health-types';

type UseHealthQueryOptions = Omit<
  UseQueryOptions<HealthStatus, Error>,
  'queryKey' | 'queryFn'
>;

export const useHealthQuery = (options?: UseHealthQueryOptions) => {
  return useQuery({
    queryKey: healthQueryKeys.status(),
    queryFn: () => getHealth(),
    ...options,
  });
};
