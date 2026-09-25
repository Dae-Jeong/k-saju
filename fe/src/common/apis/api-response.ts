/**
 * Generic response envelope. Adjust to match the backend's actual
 * response shape once it stabilizes.
 */
export interface ApiResponse<Data = unknown, Meta = unknown> {
  message: string;
  data: Data;
  meta: Meta;
}
