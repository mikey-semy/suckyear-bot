export interface LoginForm {
    username: string;
    password: string;
}

export interface LoginCredentials {
    username: string;
    password: string;
}

export interface User {
    id: number;
    username: string;
    email: string;
}

export interface LoginResponse {
    access_token: string;
    token_type: string;
    user: User | null;
}