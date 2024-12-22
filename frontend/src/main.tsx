/**
 * @module Main
 * @description Точка входа в приложение. Инициализирует роутинг и рендерит корневой компонент.
 */
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import App from './app'
import { Error, Home } from './pages'

/**
 * @constant router
 * @description Конфигурация маршрутов приложения
 */
const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <Error />,
    children: [
      {
        index: true,
        element: <Home />,
        errorElement: <Error />,
      }
    ],
  },

]);

/**
 * Рендер приложения в DOM
 * @description Монтирует приложение в элемент root с включенным StrictMode
 */
createRoot(document.getElementById('root')!).render(
  <StrictMode>
      <RouterProvider router={router} />
  </StrictMode>,
);