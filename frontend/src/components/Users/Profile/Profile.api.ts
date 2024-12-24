import api, { handleApiResponse, handleApiError } from '@/api';
import { ProfileCredentials, ProfileResponse } from './Profile.types'; // Предполагается, что у вас есть типы для профиля

// Получение профиля пользователя
export const getUserProfile = (token: string): Promise<ProfileCredentials> =>
    api.get<ProfileCredentials>('/api/v1/users/profile', {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
    .then(handleApiResponse)
    .catch(handleApiError);

// Обновление профиля пользователя
export const updateUserProfile = (token: string, profileData: ProfileCredentials): Promise<ProfileResponse> =>
    api.put<ProfileResponse>('/api/v1/users/profile', profileData, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
    .then(handleApiResponse)
    .catch(handleApiError);