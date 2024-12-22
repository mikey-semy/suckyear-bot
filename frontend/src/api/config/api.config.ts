export const API_CONFIG = {
    BASE_URL: import.meta.env.VITE_API_URL || 'https://api.suckyea.ru',
    CREDENTIALS: {
      username: import.meta.env.VITE_API_USERNAME,
      password: import.meta.env.VITE_API_PASSWORD
    }
  } as const