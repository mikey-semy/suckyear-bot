import { css } from 'styled-components'
import { tokens } from '@/styles/themes'
import {
  ColorKey,
  SizeKey,
  SpaceKey,
  FontKey,
  WeightKey,
  RadiusKey, 
  ShadowKey,
  TransitionKey,
  ZIndexKey
} from './helpers.types'

export const t = {
  color: (key: ColorKey) => css`${({ theme }) => theme.colors[key]}`,
  size: (key: SizeKey) => tokens.sizes[key],
  space: (key: SpaceKey) => tokens.spacing[key],
  font: (key: FontKey) => tokens.typography.fontSizes[key],
  weight: (key: WeightKey) => tokens.typography.fontWeights[key],
  radius: (key: RadiusKey) => tokens.borders.radius[key],
  shadow: (key: ShadowKey) => tokens.shadows[key],
  transition: (key: TransitionKey) => tokens.transitions[key],
  zIndex: (key: ZIndexKey) => tokens.zIndexes[key]
}