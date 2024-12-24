/**
 * @module IconButtonStyles
 * @description Базовые стили для кнопок с иконками
 */
import styled from 'styled-components';
import { t } from '@/styles/helpers';
import { ButtonContainer, ButtonIcon, ButtonTitle } from './Button.styles';


/**
 * @component BaseIconButtonContainer
 * @description Базовый контейнер для иконочных кнопок
 */
export const BaseIconButtonContainer = styled(ButtonContainer)`
    height: ${t.size('iconButton')};
    width: ${t.size('iconButton')};
    text-align: center;
    transition: ${t.transition('normal')};
    box-shadow: none;
    background-color: transparent;
    
    &:hover, &:active {
        background-color: transparent;
    }
`;

/**
 * @component BaseIconButtonTitle
 * @description Скрытый текст для иконочных кнопок
 */
export const BaseIconButtonTitle = styled(ButtonTitle)`
    display: 'none';
`;

/**
 * @component BaseIconButtonIcon
 * @description Базовая иконка с общими стилями
 */
export const BaseIconButtonIcon = styled(ButtonIcon)`
    color: ${t.color('primary')};
    font-size: ${t.font('md')};
`;