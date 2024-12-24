import api, { handleApiResponse, handleApiError } from '@/api';
import { LoginCredentials, LoginResponse/*, User*/ } from './Login.types';


export const login = async (credentials: LoginCredentials): Promise<LoginResponse> => {
    const formData = new URLSearchParams();
    
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    formData.append('grant_type', 'password');
    formData.append('scope', '');
    formData.append('client_id', 'string');
    formData.append('client_secret', 'string');

    try {
        const response = await api.post<LoginResponse>('/api/v1/token', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });

        const { access_token, token_type } = handleApiResponse(response);
        localStorage.setItem('token', access_token);

        // !!! пока нет api
        // const userResponse = await api.get<User>('/api/v1/users/me', {
        //     headers: {
        //         Authorization: `Bearer ${access_token}`
        //     }
        // });

        return {
            access_token,
            token_type,
            user: null // handleApiResponse(userResponse) !!! пока нет api
        };

    } catch (error) {
        handleApiError(error);
        throw error;
    }
};