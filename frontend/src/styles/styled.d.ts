import { tokens } from './tokens'

type ThemeColors = typeof tokens.colors.light

export type ThemeType = {
  colors: ThemeColors
}