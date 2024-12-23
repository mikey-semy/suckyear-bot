import React from 'react';
import { ButtonTypes } from './Button.types';
import { ButtonContainer, ButtonIcon, ButtonTitle } from './Button.styles';

/**
 * Компонент кнопки
 *
 * @param {ButtonTypes} props - Пропсы компонента
 * @param {string} props.type - Тип кнопки (по умолчанию "button")
 * @param {function} props.onClick - Обработчик клика
 * @param {React.ReactNode} props.icon - Иконка кнопки
 * @param {string} props.title - Текст кнопки
 * @param {boolean} props.disabled - Флаг неактивного состояния
 * @param {React.ComponentType} props.as - Компонент для рендера контейнера
 * @param {React.ComponentType} props.iconAs - Компонент для рендера иконки
 * @param {React.ComponentType} props.titleAs - Компонент для рендера текста
 * @param {boolean} props.loading - Флаг состояния загрузки
 * @param {React.ReactNode} props.loadingIcon - Иконка загрузки
 * @param {string} props.loadingText - Текст загрузки
 * @param {'primary' | 'secondary'} props.variant - Вариант стиля кнопки
 * @param {boolean} props.isActive - Флаг активного состояния
 * @returns {TSX.Element} Компонент кнопки
 * 
 * @component
 * @example
 * return (
 *   <Button
 *      type="button"
 *      onClick={handleClick}
 *      icon={<Icon />}
 *      title="Нажми меня"
 *      disabled={false}
 *      as={Link}
 *      iconAs={Icon}
 *      titleAs={Text}
 *      loading={false}
 *      loadingIcon={<LoadingIcon />}
 *      loadingText = 'Загрузка...'
 *      $variant = 'primary'
 *      $isActive = false,
 *   />
 * )
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
    loadingIcon,
    loadingText = 'Загрузка...',
    $variant = 'primary',
    $isActive = false,
  }) => {
  return (
    <ButtonContainer
      as={as}
      type={type} 
      onClick={onClick as any} //! Разобраться с any
      disabled={disabled || loading}
      $variant={$variant}
      
    >
      <ButtonIcon 
        as={iconAs} 
        $isActive={$isActive}
      >
        {loading ? (
            loadingIcon || <span>{loadingText}</span> //! Изменить на React.ReactNode
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