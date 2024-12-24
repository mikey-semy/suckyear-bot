import styled from 'styled-components';
import { t } from '@/styles/helpers';
import { Container } from '@/styles';

export const FooterWrapper = styled(Container)`
    width: 100%;
    height: ${t.size('footerHeight')};
    background: ${t.color('secondary')};
    border-top: 1px solid ${t.color('gray200')};
`;

export const FooterContainer = styled.footer`
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: ${t.space('xl')};
    height: 100%;  
`;