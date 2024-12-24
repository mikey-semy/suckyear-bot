import styled from 'styled-components';
import { t } from '@/styles/helpers';

/**
 * Основная форма логина
 * 
 * Стили:
 * - Флекс-контейнер с вертикальным направлением
 * - Центрирование содержимого
 * - Максимальная ширина из темы
 * - Отступы и тени из токенов
 */

export const FormLogin = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: ${t.space('md')};
  width: 100%;
  max-width: ${t.size('maxWidthForm')};
  padding: ${t.space('xl')};
  background: ${t.color('secondary')};
  border-radius: ${t.radius('md')};
  box-shadow: ${t.shadow('md')};
`;

/**
 * Заголовок формы логина
 * 
 * Стили:
 * - Основной шрифт из темы
 * - Большой размер текста
 * - Основной цвет
 * - Центрирование
 */
export const LoginTitle = styled.h1`
  font-family: ${t.family('primary')};
  font-size: ${t.font('lg')};
  color: ${t.color('primary')};
  text-align: center;
  margin-bottom: ${t.space('md')};
`;

/**
 * Кнопка входа в систему
 * 
 * Стили:
 * - Флекс для выравнивания содержимого
 * - Фиксированная ширина из темы
 * - Текст капсом
 * - Полужирный шрифт
 */
export const LoginButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  width: ${t.size('widthButton')};
  margin: 0;
  text-transform: uppercase;
  font-weight: ${t.weight('semibold')};
  font-family: ${t.family('primary')};
`;

/**
 * Иконка кнопки логина (скрытая)
 */
export const LoginButtonIcon = styled.span`
  display: none;
`;

/**
 * Контейнер для отображения ошибок
 * 
 * Стили:
 * - Флекс с центрированием
 * - Автоматический отступ сверху
 * - Фиксированная высота из темы
 */
export const ErrorContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: auto;
  margin-bottom: ${t.space('xs')};
  height: ${t.size('heightInput')};
`;

/**
 * Пустой контейнер-заглушка
 * 
 * Стили:
 * - Такие же размеры как у ErrorContainer
 * - Используется для сохранения размеров формы
 */
export const EmptyContainer = styled.div`
  display: flex;
  margin-top: auto;
  margin-bottom: ${t.space('xs')};
  height: ${t.size('heightInput')};
`;