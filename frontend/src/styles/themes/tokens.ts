export const tokens = {
    colors: {
        light: {
            // Основные
            primary: '#161616',     // Главный текст, заголовки, иконки
            secondary: '#fdfdfc',    // Фон, карточки, модалки
            accent: '#404040',      // Кнопки, ссылки, выделения

            // Статусы
            success: '#808080',
            warning: '#666666',
            error: '#1a1a1a',
            info: '#4d4d4d',

            // Оттенки серого  
            gray100: '#f7f7f7',
            gray200: '#e6e6e6', 
            gray300: '#cccccc',
            gray400: '#999999',
            gray500: '#808080',
            gray600: '#666666',
            gray700: '#4d4d4d',
            gray800: '#333333',
            gray900: '#1a1a1a',

            // Взаимодействие
            hover: '#666666',
            active: '#333333',
            focus: '#4d4d4d',
            disabled: '#cccccc'
        },
        dark: {
            // Основные
            primary: '#f9f9f8',     // Светлый текст на темном фоне
            secondary: '#161616',  // Темный фон
            accent: '#b3b3b3',     // Яркий акцент для кнопок/ссылок

            // Статусы  
            success: '#808080', 
            warning: '#999999',
            error: '#e6e6e6',
            info: '#b3b3b3',

            // Оттенки серого
            gray100: '#0d0d0d',
            gray200: '#1a1a1a',
            gray300: '#333333', 
            gray400: '#4d4d4d',
            gray500: '#666666',
            gray600: '#808080',
            gray700: '#999999',
            gray800: '#b3b3b3',
            gray900: '#cccccc',

            // Взаимодействие
            hover: '#999999',
            active: '#cccccc',
            focus: '#b3b3b3', 
            disabled: '#333333'
        }
    },
    
    sizes: {
        headerHeight: '80px',
        iconButton: '36px',
        searchHeight: '48px',
        input: '40px',
        button: {
            sm: '32px',
            md: '40px', 
            lg: '48px',
            xl: '56px'
        },
        avatar: {
            xs: '24px',
            sm: '32px',
            md: '40px',
            lg: '56px',
            xl: '80px'
        },
        modal: {
            sm: '400px',
            md: '600px', 
            lg: '800px',
            xl: '1000px'
        }
    },
    
    spacing: {
        xxs: '2px',
        xs: '4px',
        sm: '8px',
        md: '16px',
        lg: '24px',
        xl: '32px',
        xxl: '48px',
        section: '64px'
    },

    typography: {

        fontFamily: {
            primary: 'Inter, -apple-system, sans-serif',
            secondary: 'Roboto, sans-serif',
        },

        fontSizes: {
            xxs: '10px',  // Мелкий шрифт
            xs: '12px',   // Подписи
            sm: '14px',   // Основной текст
            md: '16px',   // Параграфы
            lg: '20px',   // Подзаголовки
            xl: '24px',   // Заголовки
            xxl: '32px',  // Крупные заголовки
            hero: '48px'  // Для героических секций
        },

        fontWeights: {
            thin: 100,
            light: 300, 
            regular: 400,
            medium: 500,
            semibold: 600,
            bold: 700,
            black: 900
        },

        lineHeights: {
            compact: 1,      // Для заголовков
            tight: 1.2,      // Для подзаголовков
            normal: 1.5,     // Для текста
            loose: 1.8,      // Для длинных текстов
            article: 2       // Для статей
        }
    },

    borders: {
        radius: {
            none: '0',
            xs: '2px',
            sm: '4px', 
            md: '8px',
            lg: '16px',
            xl: '24px',
            round: '50%',
            pill: '9999px'
        },
        width: {
            none: '0',
            hairline: '0.5px',
            thin: '1px',
            medium: '2px',
            thick: '4px',
            heavy: '8px'
        }
    },

    shadows: {
        none: 'none',
        inner: 'inset 0 2px 4px rgba(0,0,0,0.06)',
        xs: '0 1px 2px rgba(0,0,0,0.05)',
        sm: '0 1px 3px rgba(0,0,0,0.12)',
        md: '0 4px 6px rgba(0,0,0,0.12)',
        lg: '0 10px 15px rgba(0,0,0,0.12)',
        xl: '0 20px 25px rgba(0,0,0,0.12)',
        xxl: '0 25px 50px rgba(0,0,0,0.15)'
    },

    transitions: {
        instant: '0.1s ease',
        fast: '0.2s ease',
        normal: '0.3s ease',
        slow: '0.5s ease',
        slower: '0.7s ease',
        bounce: '0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55)',
        elastic: '0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)'
    },

    breakpoints: {
        xs: '320px',     // Старые мобилки
        sm: '430px',     // Современные телефоны
        md: '768px',     // Планшеты
        lg: '1024px',    // Ноуты
        xl: '1440px',    // Мониторы
        xxl: '1920px',   // 4К и выше
        ultrawide: '2560px' // Для богатых
    },

    zIndexes: {
        hide: -1,
        base: 0,
        dropdown: 100,
        sticky: 200,
        header: 300,
        modal: 400,
        popover: 500,
        toast: 600,
        tooltip: 700
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