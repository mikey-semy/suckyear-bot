import styled from 'styled-components';
import { ButtonContainer, ButtonIcon, ButtonTitle } from '@/components/Common/Button/Button.styles';
import { t } from '@/styles/helpers';

export const SortContainer = styled.div`
    display: flex;
    gap: ${t.space('sm')};
    margin-bottom: ${t.space('md')};
`;

/**
 * @component SortButtonContainer
 * @description Контейнер кнопки с фиксированными размерами
 * @extends ButtonContainer
 */
export const SortButtonContainer = styled(ButtonContainer)`
    height: ${t.size('iconButton')};
    width: ${t.size('iconButton')};
    text-align: center;
    transition: ${t.transition('normal')};
    box-shadow: none;
    background-color: transparent;
`;

/**
 * @component SortButtonTitle
 * @description Скрытый текст кнопки
 * @extends ButtonTitle
 */
export const SortButtonTitle = styled(ButtonTitle)`
    display: 'none';
`;

/**
 * @component SortButtonIcon
 * @description Иконка сортировки постов
 * @extends ButtonIcon
 */
export const SortButtonIcon = styled(ButtonIcon)<{ $isActive?: boolean }>`
    color: ${t.color('gray300')};
    font-size: ${t.font('md')};

    &:hover {
        color: ${t.color('gray400')};
    }
   
    &:active {
        color: ${t.color('gray500')};
    }

    ${({ $isActive }) => $isActive && `
        color: ${t.color('error')};
        font-weight: bold;
    `}

`;