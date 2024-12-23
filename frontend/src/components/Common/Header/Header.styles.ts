/**
 * @module HeaderStyles
 * @description Стилизованные компоненты для шапки приложения
 */
import styled from 'styled-components';
import { t } from '@/styles/helpers';

/**
 * @component HeaderContainer
 * @description Контейнер шапки с фиксированной высотой и выравниванием элементов по правому краю
 */
export const HeaderContainer = styled.header`
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: ${t.space('xl')};
    height: ${t.size('headerHeight')};
    padding: 0 ${t.space('lg')};
    width: 100%;
    background: ${t.color('secondary')};
    z-index: ${t.zIndex('header')};
`;


/**
 * @component RightButtonsContainer
 * @description Контейнер для группы кнопок в правой части шапки
 */
export const RightButtonsContainer = styled.div`
    display: flex;
    gap: ${t.space('sm')};
`;

