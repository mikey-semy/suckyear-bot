import styled from 'styled-components';
import { t } from '@/styles';
import { 
    BaseIconButtonContainer, 
    BaseIconButtonTitle, 
    BaseIconButtonIcon 
  } from '@/components/Common/Button/IconButton.styles';
  
export const SortContainer = styled.div`
    display: flex;
    gap: ${t.space('sm')};
    margin-bottom: ${t.space('md')};
`;

export const SortButtonContainer = styled(BaseIconButtonContainer)``;
export const SortButtonTitle = styled(BaseIconButtonTitle)``;
export const SortButtonIcon = styled(BaseIconButtonIcon)<{ $isActive?: boolean }>`
    color: ${t.color('gray300')};
    font-size: ${t.font('md')};

    &:hover {
        color: ${t.color('gray400')};
    }
   
    &:active {
        color: ${t.color('gray500')};
    }

    ${({ $isActive }) => $isActive && `
        color: ${t.color('error')};
        font-weight: bold;
    `}
`;

