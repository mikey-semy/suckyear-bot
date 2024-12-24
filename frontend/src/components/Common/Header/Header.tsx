import React from 'react';
import { HeaderContainer, HeaderWrapper, RightButtonsContainer} from './Header.styles';
import { ThemeButton } from './Buttons';
import { Logo } from '@/components';

const Header: React.FC = () => {

    return (
        <HeaderWrapper>
            <HeaderContainer>
                <Logo />
                <RightButtonsContainer>        
                    <ThemeButton />
                </RightButtonsContainer>
            </HeaderContainer>
        </HeaderWrapper>
    )
}
export default Header;