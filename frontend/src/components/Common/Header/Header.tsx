import React from 'react';
import { HeaderContainer, RightButtonsContainer} from './Header.styles';
import { ThemeButton } from './Buttons';


const Header: React.FC = () => {

    return (
        <>
            <HeaderContainer>
                <RightButtonsContainer>        
                    <ThemeButton />
                </RightButtonsContainer>
            </HeaderContainer>
        </>
    )
}
export default Header;