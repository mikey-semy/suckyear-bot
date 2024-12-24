import styled from 'styled-components';

export const SelectContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
`;

export const Select = styled.select<{ hasError?: boolean }>`
    width: 280px;
    padding: 8px 12px;
    border: 1px solid var(--input-border-color);
    border-radius: var(--border-radius-default);
    box-shadow: var(--box-shadow-default);
    background-color: var(--input-background);
    color: var(--input-color);
    font-size: 14px;
    outline: none;
    margin-bottom: 20px;

    &:focus {
        border-color: var(--input-focus-color);
    }
    
    &:disabled {
        background-color: var(--input-disabled-background);
        color: var(--input-disabled-color);
        cursor: not-allowed;
    }
`;

export const Option = styled.option`
    padding: 8px;
    font-size: 14px;
    background-color: var(--input-background);
    color: var(--input-color);
`;

export const ErrorMessage = styled.span`
    position: absolute;
    display: block;
    bottom: 5px;
    color: var(--error-color);
    font-size: 10px;
    margin-top: 4px;
`;