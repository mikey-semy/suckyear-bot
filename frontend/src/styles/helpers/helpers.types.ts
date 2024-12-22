import { tokens } from '@/styles/themes'

type ColorMode = keyof typeof tokens.colors
type ThemeColors = typeof tokens.colors[ColorMode]

export type ColorKey = keyof ThemeColors
export type SizeKey = keyof typeof tokens.sizes
export type SpaceKey = keyof typeof tokens.spacing
export type FontKey = keyof typeof tokens.typography.fontSizes
export type WeightKey = keyof typeof tokens.typography.fontWeights
export type RadiusKey = keyof typeof tokens.borders.radius
export type ShadowKey = keyof typeof tokens.shadows
export type TransitionKey = keyof typeof tokens.transitions
export type ZIndexKey = keyof typeof tokens.zIndexes