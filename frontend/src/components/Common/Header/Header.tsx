import React from 'react';
import { HeaderContainer, RightButtonsContainer} from './Header.styles';
import { ThemeButton } from './Buttons';
import { Logo } from '@/components';

const Header: React.FC = () => {

    return (
        <>
            <HeaderContainer>
                <Logo 

                />
                <RightButtonsContainer>        
                    <ThemeButton />
                </RightButtonsContainer>
            </HeaderContainer>
        </>
    )
}
export default Header;