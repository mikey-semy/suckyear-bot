import styled from 'styled-components';

export const AppContainer = styled.div`
    /* overscroll-behavior-x: none;
    touch-action: pan-y pinch-zoom; // Разрешаем только вертикальный скролл */

    display: flex;
    height: 100vh;
    width: 100vw;

    @media (max-width: 1024px) {
        height: 100%;
        width: 100%;
    }
`;

export const MainContainer = styled.div`
    display: flex;
    flex-direction: column;
    flex: 1;
    
`;