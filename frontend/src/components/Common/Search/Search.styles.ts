import styled, { keyframes } from 'styled-components';
import { t } from '@/styles/helpers';

const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

export const SearchContainer = styled.div`
    position: relative;
    display: flex;
    align-items: center;
    height: ${t.size('searchHeight')};
    margin-bottom: ${t.space('md')};
`;

export const SearchLoadingContainer = styled.div`
    animation: ${fadeIn} ${t.transition('slow')};
    padding: 20px;
    text-align: center;
    color: ${({ theme }) => theme.colors.text};
`;

export const SearchInput = styled.input`
    
    width: 100%;
    padding: ${t.space('sm')};
    font-size: ${t.font('md')};
    color: ${t.color('primary')};
    background: transparent;
    border: none;
    border-bottom: 1px solid ${t.color('gray200')};
    transition: ${t.transition('normal')};
    padding: ${t.space('md')} ${t.space('xl')};
    &:focus {
        outline: none;
        border-bottom-color: ${t.color('gray400')};
    }

    &::placeholder {
        color: ${t.color('gray300')};
    }
`;

export const SearchIcon = styled.span`
    position: absolute;
    left: 12px;
    color: ${t.color('primary')};
    pointer-events: none;
`;

export const ClearButton = styled.button`
    position: absolute;
    right: 12px;
    background: none;
    border: none;
    cursor: pointer;
    color: ${t.color('primary')};
    
    &:hover {
        color: var(--color-text-primary);
    }
`;