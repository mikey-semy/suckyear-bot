/**
 * @module HeaderStyles
 * @description Стилизованные компоненты для шапки приложения
 */
import styled from 'styled-components';
import { t } from '@/styles/helpers';
import { Container } from '@/styles';

/**
 * @component HeaderContainer
 * @description Контейнер шапки с фиксированной высотой и выравниванием элементов по правому краю
 */
export const HeaderWrapper = styled.header`
    width: 100%;
    height: ${t.size('headerHeight')};
    background: ${t.color('secondary')};
    z-index: ${t.zIndex('header')};
`;

export const HeaderContainer = styled(Container)`
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: ${t.space('xl')};
    height: 100%;
`;
/**
 * @component RightButtonsContainer
 * @description Контейнер для группы кнопок в правой части шапки
 */
export const RightButtonsContainer = styled.div`
    display: flex;
    gap: ${t.space('sm')};
`;

