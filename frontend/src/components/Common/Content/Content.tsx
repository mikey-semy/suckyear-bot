import React from 'react';
import { ContentProps } from './Content.types';
import { ContentContainer, ContentWrapper } from './Content.styles';


const Content: React.FC<ContentProps> = ({ children }) => {

    return (
        <ContentWrapper>
            <ContentContainer>
                {children}
            </ContentContainer>
        </ContentWrapper>
    );
};

export default Content;
