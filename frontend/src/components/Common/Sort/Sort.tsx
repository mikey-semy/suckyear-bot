import React from 'react';
import { SortContainer, SortButtonContainer, SortButtonIcon } from './Sort.styles';
import { SortTypes } from './Sort.types';
import { Button } from '@/components';
import { MdCalendarToday, MdOutlineStar } from 'react-icons/md';

const Sort: React.FC<SortTypes> = ({ onSort, activeSort }) => {

    return (
        <SortContainer>
            <Button
                as={SortButtonContainer}
                iconAs={SortButtonIcon}
                onClick={() => onSort('created_at')}
                icon={MdCalendarToday}
                $isActive={activeSort === 'created_at'}
            />
            <Button
                as={SortButtonContainer}
                iconAs={SortButtonIcon}
                onClick={() => onSort('rating')}
                icon={MdOutlineStar}
                $isActive={activeSort === 'rating'}
            />
        </SortContainer>
    );
}
export default Sort;