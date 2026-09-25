import { AxiosError } from 'axios';

export interface ApiErrorBody {
  errorCode: string;
  message: string | null;
  detail: string | null;
}

export class ApiError extends AxiosError<ApiErrorBody> {
  constructor(error: AxiosError<ApiErrorBody>) {
    super();
    Object.assign(this, error);
  }
}
