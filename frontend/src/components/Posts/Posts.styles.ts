import styled from 'styled-components';
import { t } from '@/styles/helpers';

export const PostsContainer = styled.div`
    display: flex;
    flex-direction: column;
    margin: 0 100px;
    height: 100%;
    min-height: 90vh;

    @media (max-width: ${t.breakpoints('sm')}) {
            margin: 0 20px;
        }
`;