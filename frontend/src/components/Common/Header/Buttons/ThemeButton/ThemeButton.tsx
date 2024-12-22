import React from 'react';
import { Button } from '@/components';
import { useTheme } from '@/contexts';
import { BsSun, BsMoon } from "react-icons/bs";
import { ThemeButtonContainer, ThemeButtonIcon } from './ThemeButton.styles';

const ThemeButton: React.FC = () => {
    const { isDark, toggleTheme } = useTheme();

    return (
        <Button 
            as={ThemeButtonContainer}
            iconAs={ThemeButtonIcon}
            onClick={toggleTheme}
            icon={isDark ? BsMoon : BsSun }
        />
    );

};
export default ThemeButton;