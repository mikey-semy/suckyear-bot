import styled from 'styled-components';

export const ErrorContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 24px;
    height: 90vh;
`;

export const ErrorButton = styled.button`
    padding: 12px 24px;
    border-radius: 8px;
    background: var(--button-background, #007bff);
    color: var(--button-color, #fff);
    border: none;
    cursor: pointer;
    transition: all var(--transition-default);

    &:hover {
        background: var(--button-hover-background, #0056b3);
    }
`;