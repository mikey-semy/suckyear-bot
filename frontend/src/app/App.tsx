/**
 * @module App
 * @description Корневой компонент приложения
 */
import React from 'react';
import { Outlet } from "react-router-dom";
import { ThemeProvider as StyledThemeProvider } from 'styled-components';
import { ThemeProvider, useTheme, AuthProvider } from '@/contexts';
import { Header, Footer, Content } from '@/components';
import { GlobalStyles, ResetStyles, Variables, LightTheme, DarkTheme } from '@/styles';
import { AppContainer, MainContainer } from './App.styles';

/**
 * @component AppContent
 * @description Внутренний компонент с основным контентом и темизацией
 * @returns {JSX.Element} Разметка приложения с подключенными стилями и темой
 */
const AppContent: React.FC = () => {
  const { isDark } = useTheme();

  return (
    <StyledThemeProvider theme={isDark ? DarkTheme : LightTheme}>
      <GlobalStyles />
      <ResetStyles />
      <Variables />
      <AppContainer>
            <MainContainer>
              <Header />
                <Content>
                  <Outlet />
                </Content>
              <Footer />
            </MainContainer>
      </AppContainer>
    </StyledThemeProvider>
  );
};

/**
 * @component App
 * @description Корневой компонент-обертка с провайдерами
 * @returns {JSX.Element} Приложение с подключенными провайдерами
 * @example
 * <App />
 */
const App: React.FC = () => {
  
  return (
    <AuthProvider>
      <ThemeProvider>
        <AppContent />
      </ThemeProvider>
    </AuthProvider>
  );
};
export default App;
