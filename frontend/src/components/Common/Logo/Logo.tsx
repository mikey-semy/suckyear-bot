import React from 'react';
import { LogoContainer, LogoLink, LogoText } from './Logo.styles';
import { LogoData } from './Logo.data';

const Logo: React.FC = () => {
    return (
        <LogoContainer>
            <LogoLink to={LogoData.path}>
                <LogoText>
                    <span>{LogoData.text}</span>
                </LogoText>
            </LogoLink>
        </LogoContainer>
    )
}
export default Logo;