/**
 * @module ThemeButtonStyles
 * @description Стилизованные компоненты для кнопки переключения темы
 */
import styled from 'styled-components';
import { ButtonContainer, ButtonIcon, ButtonTitle } from '@/components/Common/Button/Button.styles';
import { t } from '@/styles/helpers';

/**
 * @component ThemeButtonContainer
 * @description Контейнер кнопки с фиксированными размерами
 * @extends ButtonContainer
 */
export const ThemeButtonContainer = styled(ButtonContainer)`
    height: ${t.size('iconButton')};
    width: ${t.size('iconButton')};
    text-align: center;
    transition: ${t.transition('normal')};
    box-shadow: none;
    background-color: transparent;
    &:hover {
        background-color: transparent;
    }
    
    &:active {
        background-color: transparent;
    }

`;

/**
 * @component ThemeButtonTitle
 * @description Скрытый текст кнопки
 * @extends ButtonTitle
 */
export const ThemeButtonTitle = styled(ButtonTitle)`
    display: 'none';
`;

/**
 * @component ThemeButtonIcon
 * @description Иконка переключения темы
 * @extends ButtonIcon
 */
export const ThemeButtonIcon = styled(ButtonIcon)`
    color: ${t.color('primary')};
    font-size: ${t.font('md')};
`;