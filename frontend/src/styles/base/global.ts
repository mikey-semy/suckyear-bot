import { createGlobalStyle } from 'styled-components';
import { t } from '@/styles/helpers';

export const Global = createGlobalStyle`

    background-color: ${t.color('secondary')};
`;
export default Global;