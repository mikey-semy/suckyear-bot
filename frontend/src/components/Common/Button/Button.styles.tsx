/**
 * Стилизованные компоненты для кнопки
 * 
 * ButtonContainer - Основной контейнер кнопки
 * @param {string} variant - Вариант стиля (primary/secondary)
 * 
 * ButtonIcon - Контейнер для иконки
 * 
 * ButtonTitle - Контейнер для текста
 * 
 * Использует дизайн-токены для:
 * - Отступов (space)
 * - Цветов (color) 
 * - Скруглений (radius)
 * - Теней (shadow)
 * - Прозрачности (opacity)
 * - Анимаций (transition)
 */
import styled from 'styled-components';
import { t } from '@/styles/helpers';

/**
 * Основной контейнер кнопки
 * @component
 * @param {Object} props
 * @param {'primary' | 'secondary'} props.variant - Определяет цветовую схему кнопки
 * 
 * Стили:
 * - Flexbox контейнер с центрированием
 * - Отступы и промежутки из токенов
 * - Цвета фона и текста зависят от варианта
 * - Анимации при наведении/нажатии
 * - Состояния hover/active/disabled
 */
export const ButtonContainer = styled.button<{ $variant?: 'primary' | 'secondary'}>`
    display: flex;
    align-items: center;
    
    gap: ${t.space('sm')};
    padding: 10px;

    color: ${({ $variant }) => 
        $variant === 'primary' ? t.color('primary') : t.color('secondary')};
    
    border: none;
    
    transition: ${t.transition('normal')};
    cursor: pointer;

    &:hover {
        opacity: ${t.opacity(90)};
    }
    
    &:active {
        
    }

    &:disabled {
        opacity: ${t.opacity(50)};
        cursor: not-allowed;
    }

    
`;

/**
 * Контейнер для иконки кнопки
 * @component
 * 
 * Стили:
 * - Flexbox с центрированием
 * - Наследует цвет от родителя
 */
export const ButtonIcon = styled.span<{ $isActive?: boolean }>`
    display: flex;
    align-items: center;
    color: inherit;

    ${({ $isActive }) => $isActive && `
        color: ${t.color('accent')};
    `}
`;

/**
 * Контейнер для текста кнопки
 * @component
 * 
 * Стили:
 * - Блочный элемент
 * - Наследует цвет от родителя
 * - Плавная анимация изменений
 */
export const ButtonTitle = styled.span`
    display: block;
    color: inherit;
    transition: ${t.transition('normal')};
`;