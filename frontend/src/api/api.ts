/**
 * Клиент для работы с API SuckYear
 * 
 * @example
 * - GET запрос
 * const posts = await api.get('/posts');
 * 
 * - POST запрос с данными
 * const newPost = await api.post('/posts', {
 *   text: 'Моя история неудачи',
 *   rating: 5
 * });
 */
import axios from 'axios';
import { API_CONFIG } from './config/api.config'

/** Базовая конфигурация API клиента */
const api = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

/** 
 * Интерцептор для добавления Basic Auth в каждый запрос
 * Credentials берутся из переменных окружения:
 * - VITE_API_USERNAME
 * - VITE_API_PASSWORD
 * ! Ещё ниразу не использовал Basic Auth, 
 * ! нужно сделать через Token
 */
api.interceptors.request.use((config) => {
  config.auth = config.auth = API_CONFIG.CREDENTIALS;
  return config;
});

export default api;