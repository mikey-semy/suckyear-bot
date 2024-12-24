/**
 * @module LogoStyles
 * @description Стилизованные компоненты для логотипа
 */
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { t } from '@/styles/helpers';

/**
 * @component LogoContainer
 * @description Контейнер для логотипа с фиксированной высотой
 */
export const LogoContainer = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
`;

/**
 * @component LogoLink
 * @description Кликабельная область логотипа
 */
export const LogoLink = styled(Link)`
    display: flex;
    align-items: center;
    justify-content: center;
    
    user-select: none;
    -webkit-user-drag: none;
    -webkit-tap-highlight-color: transparent;
`;

/**
 * @component LogoText
 * @description Текстовая часть логотипа
 */
export const LogoText = styled.span`
    display: inline-block;
    vertical-align: middle;
    position: relative;
    font-family: ${t.family('primary')};
    font-size: ${t.font('xl')};
    font-weight: ${t.weight('bold')};
    color: ${t.color('primary')};

    user-select: none;
    -webkit-user-drag: none;
    letter-spacing:  ${t.space('xs')};
    transition: ${t.transition('normal')};

    white-space: nowrap;
`;