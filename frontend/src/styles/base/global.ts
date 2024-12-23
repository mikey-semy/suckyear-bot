import { createGlobalStyle } from 'styled-components';
import { t } from '@/styles/helpers';

export const Global = createGlobalStyle`

    body {
        font-family: ${t.family('primary')};
        font-size: ${t.font('md')};
        font-weight: ${t.weight('regular')};
        line-height: ${t.lineHeight('normal')};
        color: ${t.color('primary')};
        background-color: ${t.color('secondary')};
    }
`;
export default Global;