import { useMutation, type UseMutationOptions } from '@tanstack/react-query';

import { type ApiResponse } from '@/common/apis/api-response';

export type UseApiMutationOptions<
  TData = unknown,
  TMeta = unknown,
  TError = Error,
  TParams = void,
  TContext = unknown,
> = UseMutationOptions<ApiResponse<TData, TMeta>, TError, TParams, TContext>;

export const useApiMutation = <
  TData = unknown,
  TMeta = unknown,
  TError = Error,
  TParams = void,
  TContext = unknown,
>(
  options: UseApiMutationOptions<TData, TMeta, TError, TParams, TContext>,
) => {
  const { data, ...restResult } = useMutation(options);

  return {
    data: data?.data ?? null,
    message: data?.message ?? null,
    meta: data?.meta ?? null,
    ...restResult,
  };
};
