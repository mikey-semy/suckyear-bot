import styled, { keyframes } from 'styled-components';
import { t } from '@/styles/helpers';

const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

export const LoadingContainer = styled.div<{ $visible: boolean }>`
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    min-height: 200px;

    animation: ${fadeIn} ${t.transition('slow')};

    opacity: ${({ $visible }) => ($visible ? 1 : 0)};
    visibility: ${({ $visible }) => ($visible ? 'visible' : 'hidden')};
    transition: opacity ${t.transition('slow')}, visibility ${t.transition('slow')};

    span {
        margin-left: 10px;
    }
`;







