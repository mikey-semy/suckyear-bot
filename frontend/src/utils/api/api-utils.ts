import { AxiosError } from 'axios';

export type ApiResponse<T> = {
    data: T;
    status: number;
};

export type ApiError = {
    message: string;
    status: number;
};

export const handleApiError = (error: unknown): never => {
    if (error instanceof AxiosError) {
        const apiError: ApiError = {
            message: error.response?.data.message || 'Неизвестная ошибка',
            status: error.response?.status || 500
        };
        console.error('API Error:', apiError);
        throw apiError;
    }
    throw error;
};

export const handleApiResponse = <T>(response: ApiResponse<T>): T => {
    if (response.status >= 200 && response.status < 300) {
        return response.data;
    }
    throw new Error(`Unexpected response status: ${response.status}`);
};