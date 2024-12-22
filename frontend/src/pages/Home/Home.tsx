import React from 'react';
import { HomeContainer } from "./Home.styles";
import { Posts } from '@/components';

const Home: React.FC = () => {

    return (
        <HomeContainer>
            <Posts />
        </HomeContainer>
    );
} 
export default Home;