import styled from 'styled-components';

export const ButtonContainer = styled.button`
    cursor: pointer;
    border: none;
    background: var(--button-background, transparent);
    color: var(--button-color);
    padding: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all var(--transition-default);
    margin-left: 10px;
    border-radius: var(--border-radius-default, 5px);
    box-shadow: var(--box-shadow-default);

    &:hover {
        background: var(--button-hover-background);
        color: var(--button-hover-color);
        opacity: 0.7;
    }

    &:active {
        background: var(--button-active-background);
        color: var(--button-active-color);
    }

    &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
`;

export const ButtonIcon = styled.span`
    display: flex;
    align-items: center;
    color: inherit;
`;

export const ButtonTitle = styled.span`
    display: block;
    color: inherit;
    transition: all 0.3s ease;
`;