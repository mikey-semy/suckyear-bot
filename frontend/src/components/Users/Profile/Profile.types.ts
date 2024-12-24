export interface ProfileForm {
    username: string;
    email: string;
  }

export interface ProfileCredentials {
    username: string;
    email: string;
}

export interface ProfileResponse {
    id: number;
    username: string;
    email: string;
}

export interface UpdateProfileResponse {
    success: boolean;
    message?: string; // Сообщение об успешном обновлении или ошибке
}