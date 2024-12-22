import { createGlobalStyle } from 'styled-components';

import { tokens } from '../themes/tokens'

const Variables = createGlobalStyle`
  :root {
    ${Object.entries(tokens.colors.light).map(
      ([key, value]) => `--color-${key}: ${value};`
    ).join('\n')}
  }
`
export default Variables