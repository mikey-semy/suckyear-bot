export interface RouteError {
    statusText?: string;
    message?: string;
}

export interface ErrorTypes {
    error?: RouteError;
}

export interface ErrorMessages {
    icon: string;
    title: string;
    description: string;
}