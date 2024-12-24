export interface RegisterForm {
    username: string;
    email: string;
    password: string;
  }

export interface RegisterCredentials {
    username: string;
    password: string;
    email: string;
}

export interface RegisterResponse {
    id: number;
    username: string;
    email: string;
}