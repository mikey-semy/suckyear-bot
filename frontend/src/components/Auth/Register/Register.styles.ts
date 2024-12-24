import styled from "styled-components";

export const FormRegister = styled.form`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 20px;
    width: 100%;
    max-width: 400px;
    padding: 40px;
    background: var(--content-background);
    border-radius: var(--border-radius-default);
    box-shadow: var(--box-shadow-default);
`;

export const RegisterTitle = styled.h1`
    font-family: var(--content-header-font);
    font-size: 24px;
    color: var(--content-header-color);
    text-align: center;
    margin-bottom: 20px;
`;

export const RegisterButton = styled.button`
    display: flex;
    justify-content: center;
    align-items: center;
    width: 140px;
    margin: 0;
    text-transform: uppercase;
    font-weight: 600;
    font-family: var(--logo-font);
`;

export const RegisterButtonIcon = styled.span`
    display: none;
`;

export const ErrorContainer = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: auto;
    margin-bottom: 10px;
    height: 40px;
`;

export const EmptyContainer = styled.div`
    display: flex;
    margin-top: auto;
    margin-bottom: 10px;
    height: 40px;
`;