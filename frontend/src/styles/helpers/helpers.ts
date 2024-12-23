import { css } from 'styled-components'
import { tokens } from '@/styles/themes'
import {
  ColorKey,
  SizeKey,
  SpaceKey,
  FamilyKey,
  FontKey,
  WeightKey,
  RadiusKey, 
  ShadowKey,
  TransitionKey,
  BreakpointKey,
  LineHeightKey,
  ZIndexKey,
  OpacityKey
} from './helpers.types'

export const t = {
  color: (key: ColorKey) => css`${({ theme }) => theme.colors[key]}`,
  size: (key: SizeKey) => tokens.sizes[key],
  space: (key: SpaceKey) => tokens.spacing[key],
  family: (key: FamilyKey) => tokens.typography.fontFamily[key],
  font: (key: FontKey) => tokens.typography.fontSizes[key],
  weight: (key: WeightKey) => tokens.typography.fontWeights[key],
  radius: (key: RadiusKey) => tokens.borders.radius[key],
  shadow: (key: ShadowKey) => tokens.shadows[key],
  transition: (key: TransitionKey) => tokens.transitions[key],
  breakpoints: (key: BreakpointKey) => tokens.breakpoints[key],
  lineHeight: (key: LineHeightKey) => tokens.typography.lineHeights[key],
  zIndex: (key: ZIndexKey) => tokens.zIndexes[key],
  opacity: (key: OpacityKey) => tokens.opacity[key]
}