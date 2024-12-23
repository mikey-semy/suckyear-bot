import React from 'react';
import { emptyMessages } from './Empty.data';
import { EmptyContainer, EmptyIcon, EmptyTitle, EmptyDescription } from './Empty.styles';

const Empty: React.FC = () => {

    return (
            <EmptyContainer>
                <EmptyIcon>{ emptyMessages.icon }</EmptyIcon>
                <EmptyTitle>{ emptyMessages.title }</EmptyTitle>
                <EmptyDescription>{ emptyMessages.description }</EmptyDescription>
            </EmptyContainer>
    );
}
export default Empty;