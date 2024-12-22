import React from 'react';
import { ContentProps } from './Content.types';
import { ContentContainer } from './Content.styles';


const Content: React.FC<ContentProps> = ({ children }) => {

    return (
        <>
            <ContentContainer>
                {children}
            </ContentContainer>
        </>
    );
};

export default Content;
