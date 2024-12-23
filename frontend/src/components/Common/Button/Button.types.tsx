/**
 * Типы для компонента Button
 * 
 * @interface ButtonTypes
 * @property {string} type - Тип кнопки HTML
 * @property {() => void} onClick - Обработчик клика
 * @property {React.ReactNode} icon - Иконка кнопки
 * @property {string} title - Текст кнопки
 * @property {boolean} disabled - Состояние блокировки
 * @property {React.ComponentType} as - Компонент-обертка
 * @property {React.ComponentType} iconAs - Компонент для иконки
 * @property {React.ComponentType} titleAs - Компонент для текста
 * @property {boolean} loading - Состояние загрузки
 * @property {React.ReactNode} loadingIcon - Иконка загрузки
 * @property {string} loadingText - Текст загрузки
 * @property {'primary' | 'secondary'} $variant - Вариант стиля
 * @property {boolean} $isActive - Активное состояние
 */
import { IconType } from 'react-icons';

export interface ButtonTypes {
    type?: "submit" | "reset" | "button";
    onClick?: ((
        event: React.FormEvent<HTMLFormElement> 
        | React.MouseEvent<HTMLButtonElement>) => void) 
        | void;
    icon?: IconType | React.ReactNode;
    title?: string | React.ReactNode;
    disabled?: boolean;
    as?: React.ComponentType;
    iconAs?: React.ComponentType; 
    titleAs?: React.ComponentType;
    loading?: boolean;
    loadingIcon?: React.ReactNode;
    loadingText?: string;
    $variant?: 'primary' | 'secondary';
    $isActive?: boolean;
}