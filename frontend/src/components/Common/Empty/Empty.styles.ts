import styled from 'styled-components';

export const EmptyContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 0 20px;
    text-align: center;
    color: var(--empty-color, #000000);
    margin: 24px;
`;

export const EmptyIcon = styled.span`
    font-size: 48px;
    margin-bottom: 16px;
`;

export const EmptyTitle = styled.span`
    font-size: 24px;
    margin-bottom: 16px;
`;

export const EmptyDescription = styled.span`
    font-size: 16px;
    margin-bottom: 16px;
`;