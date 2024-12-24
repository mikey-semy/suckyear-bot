import api, { handleApiResponse, handleApiError } from '@/api';
import { RegisterCredentials, RegisterResponse } from './Register.types';

export const register = (credentials: RegisterCredentials): Promise<RegisterResponse> =>
    api.post<RegisterResponse>('/api/v1/users', credentials)
        .then(handleApiResponse)
        .catch(handleApiError);
