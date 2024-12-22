import React from 'react';
import { ButtonTypes } from './Button.types';
import { ButtonContainer, ButtonIcon, ButtonTitle } from './Button.styles';

/**
 * Компонент кнопки
 *
 * @param {ButtonTypes} props - Объект с пропами кнопки
 * @param {string} props.type - Тип кнопки (по умолчанию "button")
 * @param {function} props.onClick - Функция, вызываемая при клике на кнопку
 * @param {React.ReactNode} props.icon - Иконка кнопки
 * @param {string} props.title - Текст кнопки
 * @param {boolean} props.disabled - Флаг, указывающий на то, что кнопка неактивна (по умолчанию false)
 * @param {React.ComponentType} props.as - Компонент, который будет использован вместо ButtonContainer
 * @param {React.ComponentType} props.iconAs - Компонент, который будет использован вместо ButtonIcon
 * @param {React.ComponentType} props.titleAs - Компонент, который будет использован вместо ButtonTitle
 *
 * @returns {TSX.Element} Компонент кнопки
 */
const Button: React.FC<ButtonTypes> = ({ 
    type = "button", 
    onClick, 
    icon: Icon, 
    title, 
    disabled = false,
    as,
    iconAs,
    titleAs,
    loading = false,
    loadingIcon
  }) => {
  return (
    <ButtonContainer
      as={as}
      type={type} 
      onClick={onClick as any} 
      disabled={disabled || loading}
    >
      <ButtonIcon as={iconAs}>
        {loading ? (
            loadingIcon || <span>Загрузка...</span>
          ) : (
            Icon && (typeof Icon === 'function' ? <Icon /> : Icon)
          )}
      </ButtonIcon>
      <ButtonTitle as={titleAs}>
        {title}
      </ButtonTitle>
    </ButtonContainer>
  );
};

export default Button;