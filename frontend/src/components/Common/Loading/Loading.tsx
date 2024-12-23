import React, { useState, useEffect } from 'react';
import { LoadingContainer } from './Loading.styles';
import { LoadingTypes } from './Loading.types';
import { BeatLoader } from 'react-spinners';
import { useTheme } from '@/contexts';

const Loading: React.FC<LoadingTypes> = ({ 
    size = 15, 
    text 
}) => {
    const { isDark } = useTheme();
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setVisible(true), 60);
        return () => clearTimeout(timer);
    }, []);

    return (
        <LoadingContainer $visible={visible}>
            <BeatLoader 
                color={isDark ? '#c9d1d9' : '#24292f'} 
                size={size}
            />
            {text && <span>{text}</span>}
        </LoadingContainer>
    );
}
export default Loading;