import styled from 'styled-components';

export const ErrorContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    margin-top: 24px;
`;

export const ErrorTitle = styled.h1`
    font-size: 48px;
    margin-bottom: 20px;
`;

export const ErrorText = styled.p`
    font-size: 24px;
    margin-bottom: 16px;
`;

export const ErrorMessage = styled.i`
    color: var(--accent-color);
`;