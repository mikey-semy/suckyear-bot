import { useState } from 'react';
import { ThemeContext } from './context';

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [isDark, setIsDark] = useState(() => {
        const saved = localStorage.getItem('theme');
        return saved ? JSON.parse(saved) : false;
    });

    const toggleTheme = () => {
        const newValue = !isDark;
        setIsDark(newValue);
        localStorage.setItem('theme', JSON.stringify(newValue));
    };

    return (
        <ThemeContext.Provider value={{ isDark, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};