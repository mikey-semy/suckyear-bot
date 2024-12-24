import styled from 'styled-components';
import { ButtonContainer, ButtonIcon, ButtonTitle } from '@/components/Common/Button/Button.styles';
import { t } from '@/styles/helpers';

export const PaginationContainer = styled.div`
    display: flex;
    gap: ${t.space('sm')};
    justify-content: center;
    margin-top: auto;
    margin-bottom: ${t.space('md')};
`;


/**
 * @component PaginationButtonContainer
 * @description Контейнер кнопки с фиксированными размерами
 * @extends ButtonContainer
 */
export const PaginationButtonContainer = styled(ButtonContainer)`
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
 * @component PaginationButtonTitle
 * @description Скрытый текст кнопки
 * @extends ButtonTitle
 */
export const PaginationButtonTitle = styled(ButtonTitle)`
    display: 'none';
`;

/**
 * @component PaginationButtonIcon
 * @description Иконка переключения темы
 * @extends ButtonIcon
 */
export const PaginationButtonIcon = styled(ButtonIcon)`
    color: ${t.color('primary')};
    font-size: ${t.font('md')};
`;