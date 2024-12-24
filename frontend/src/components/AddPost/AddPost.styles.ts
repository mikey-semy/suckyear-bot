import styled from 'styled-components';
import { t } from '@/styles/helpers';

export const AddPostContainer = styled.div`
    max-width: ${t.size('contentWidth')};
    margin: ${t.space('xl')} auto;
    padding: ${t.space('lg')};
    background: ${t.color('secondary')};
    border-radius: ${t.radius('md')};
    box-shadow: ${t.shadow('md')};
`;

export const AddPostForm = styled.form`
    display: flex;
    flex-direction: column;
    gap: ${t.space('md')};
    max-width: ${t.size('maxWidthForm')};
    margin: 0 auto;
`;

export const AddPostInput = styled.input`
    height: ${t.size('heightInput')};
    padding: ${t.space('sm')} ${t.space('md')};
    border: 1px solid ${t.color('gray300')};
    border-radius: ${t.radius('sm')};
    font-family: ${t.family('primary')};
    font-size: ${t.font('md')};
    transition: ${t.transition('normal')};
    
    &:focus {
        outline: none;
        border-color: ${t.color('accent')};
    }
    
    &:disabled {
        background: ${t.color('disabled')};
        cursor: not-allowed;
    }
`;

export const AddPostTextArea = styled.textarea`
    min-height: 200px;
    padding: ${t.space('md')};
    border: 1px solid ${t.color('gray300')};
    border-radius: ${t.radius('sm')};
    font-family: ${t.family('primary')};
    font-size: ${t.font('md')};
    line-height: ${t.lineHeight('normal')};
    resize: vertical;
    transition: ${t.transition('normal')};
    
    &:focus {
        outline: none;
        border-color: ${t.color('accent')};
    }
    
    &:disabled {
        background: ${t.color('disabled')};
        cursor: not-allowed;
    }
`;

export const AddPostButton = styled.button`
    width: ${t.size('widthButton')};
    height: ${t.size('heightInput')};
    background: ${t.color('accent')};
    color: ${t.color('secondary')};
    border: none;
    border-radius: ${t.radius('sm')};
    font-family: ${t.family('primary')};
    font-size: ${t.font('md')};
    font-weight: ${t.weight('medium')};
    cursor: pointer;
    transition: ${t.transition('normal')};
    
    &:hover:not(:disabled) {
        background: ${t.color('hover')};
    }
    
    &:active:not(:disabled) {
        background: ${t.color('active')};
    }
    
    &:disabled {
        opacity: ${t.opacity(50)};
        cursor: not-allowed;
    }
`;

export const ErrorMessage = styled.div`
    padding: ${t.space('md')};
    color: ${t.color('error')};
    background: ${t.color('gray100')};
    border-radius: ${t.radius('sm')};
    font-family: ${t.family('primary')};
    font-size: ${t.font('sm')};
    line-height: ${t.lineHeight('normal')};
`;