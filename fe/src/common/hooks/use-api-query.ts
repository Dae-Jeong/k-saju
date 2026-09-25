import {
  useQuery,
  useSuspenseQuery,
  type FetchQueryOptions,
  type QueryKey,
  type UseQueryOptions,
  type UseSuspenseQueryOptions,
} from '@tanstack/react-query';

import { type ApiResponse } from '@/common/apis/api-response';

export type UseApiQueryOptions<
  TData = unknown,
  TMeta = unknown,
  TError = Error,
  TParsedData = TData,
  TQueryKey extends QueryKey = readonly unknown[],
> = UseQueryOptions<
  ApiResponse<TData, TMeta>,
  TError,
  ApiResponse<TParsedData, TMeta>,
  TQueryKey
>;

export const useApiQuery = <
  TData = unknown,
  TMeta = unknown,
  TError = Error,
  TParsedData = TData,
  TQueryKey extends QueryKey = readonly unknown[],
>(
  options: UseApiQueryOptions<TData, TMeta, TError, TParsedData, TQueryKey>,
) => {
  const { data, ...restResult } = useQuery(options);

  return {
    data: data?.data ?? null,
    message: data?.message ?? null,
    meta: data?.meta ?? null,
    ...restResult,
  };
};

export type UseApiSuspenseQueryOptions<
  TData = unknown,
  TMeta = unknown,
  TError = Error,
  TParsedData = TData,
  TQueryKey extends QueryKey = readonly unknown[],
> = UseSuspenseQueryOptions<
  ApiResponse<TData, TMeta>,
  TError,
  ApiResponse<TParsedData, TMeta>,
  TQueryKey
>;

export const useApiSuspenseQuery = <
  TData = unknown,
  TMeta = unknown,
  TError = Error,
  TParsedData = TData,
  TQueryKey extends QueryKey = readonly unknown[],
>(
  options: UseApiSuspenseQueryOptions<
    TData,
    TMeta,
    TError,
    TParsedData,
    TQueryKey
  >,
) => {
  const { data, ...restResult } = useSuspenseQuery<
    ApiResponse<TData, TMeta>,
    TError,
    ApiResponse<TParsedData, TMeta>,
    TQueryKey
  >(options);

  return {
    data: data.data,
    message: data.message,
    meta: data.meta,
    ...restResult,
  };
};

export type ApiFetchQueryOptions<
  TData = unknown,
  TMeta = unknown,
  TError = Error,
  TParsedData = TData,
  TQueryKey extends QueryKey = readonly unknown[],
  TPageParam = never,
> = FetchQueryOptions<
  ApiResponse<TData, TMeta>,
  TError,
  ApiResponse<TParsedData, TMeta>,
  TQueryKey,
  TPageParam
>;
