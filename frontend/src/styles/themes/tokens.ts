export const tokens = {
    colors: {
        light: {
            // Основные
            primary: '#161616',     // Главный текст, заголовки, иконки
            secondary: '#fdfdfc',    // Фон, карточки, модалки
            accent: '#0969da',      // Кнопки, ссылки, выделения

            // Статусы
            success: '#2da44e',     // Успешные операции, галочки
            warning: '#bf8700',     // Предупреждения, уведомления
            error: '#cf222e',       // Ошибки, удаление
            info: '#0969da',        // Информационные сообщения

            // Оттенки серого  
            gray100: '#f6f8fa',     // Легкий фон
            gray200: '#eaeef2',     // Границы
            gray300: '#d0d7de',     // Неактивные элементы
            gray400: '#8c959f',     // Второстепенный текст
            gray500: '#6e7781',     // Плейсхолдеры

            // Взаимодействие
            hover: '#0969da',       // При наведении
            active: '#0550ae',      // При нажатии
            focus: '#0969da',       // При фокусе
            disabled: '#8c959f'     // Неактивные элементы
        },
        dark: {
            // Основные
            primary: '#f9f9f8',     // Светлый текст на темном фоне
            secondary: '#161616',  // Темный фон
            accent: '#2f81f7',     // Яркий акцент для кнопок/ссылок

            // Статусы  
            success: '#3fb950',
            warning: '#d29922',
            error: '#f85149', 
            info: '#58a6ff',

            // Оттенки серого
            gray100: '#161b22',
            gray200: '#21262d',
            gray300: '#30363d', 
            gray400: '#8b949e',
            gray500: '#c9d1d9',

            // Взаимодействие
            hover: '#388bfd',
            active: '#1f6feb',
            focus: '#388bfd',
            disabled: '#484f58'
        }
    },
    
    sizes: {
        headerHeight: '80px',
        iconButton: '36px',
        searchHeight: '48px'
    },
    
    spacing: {
        xs: '4px',
        sm: '8px',
        md: '16px',
        lg: '24px',
        xl: '32px'
    },

    typography: {

        fontFamily: {
            primary: 'Inter, sans-serif',
            secondary: 'Roboto, sans-serif',
        },

        fontSizes: {
            xs: '12px',
            sm: '14px',
            md: '16px',
            lg: '20px',
            xl: '24px'
        },

        fontWeights: {
            regular: 400,
            medium: 500,
            bold: 700
        },

        lineHeights: {
            tight: 1.2,
            normal: 1.5,
            loose: 1.8
        }
    },

    borders: {
        radius: {
            sm: '4px',
            md: '8px',
            lg: '16px',
            round: '50%'
        },
        width: {
            thin: '1px',
            thick: '2px'
        }
    },

    shadows: {
        sm: '0 1px 3px rgba(0,0,0,0.12)',
        md: '0 4px 6px rgba(0,0,0,0.12)',
        lg: '0 10px 20px rgba(0,0,0,0.12)'
    },

    transitions: {
        fast: '0.2s ease',
        normal: '0.3s ease',
        slow: '0.5s ease'
    },

    breakpoints: {
        mobile: '430px',
        tablet: '768px',
        desktop: '1024px',
        wide: '1440px'
    },

    zIndexes: {
        header: 100,
        modal: 200,
        dropdown: 300
    },
    opacity: {
        0: 0,
        10: 0.1,
        20: 0.2,
        30: 0.3,
        40: 0.4,
        50: 0.5,
        60: 0.6,
        70: 0.7,
        80: 0.8,
        90: 0.9,
        100: 1
    }

    
  } as const