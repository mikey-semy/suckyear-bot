import styled from 'styled-components';

export const FooterContainer = styled.footer`
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 32px;

    height: 40px;
    width: 100%;

    background: var(--footer-background, #FFFFFF);

    @media (max-width: 1024px) {
        display: none;
    }
`;