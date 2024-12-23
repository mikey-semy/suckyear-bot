import React from 'react';
import { Button } from '@/components';
import { PaginationContainer, PaginationButtonContainer, PaginationButtonIcon } from './Pagination.styles';
import { PaginationTypes } from './Pagination.types';
import { MdNavigateBefore, MdNavigateNext } from 'react-icons/md';

const Pagination: React.FC<PaginationTypes> = ({ total, limit, current, onChange }) => {

    const pages = Math.ceil(total / limit);

    return (
        <PaginationContainer>
            <Button
                as={PaginationButtonContainer}
                iconAs={PaginationButtonIcon}
                onClick={() => onChange(current - 1)}
                icon={<MdNavigateBefore />}
                disabled={current === 1}
            />
            {Array.from({ length: pages }, (_, index) => (
                <Button 
                    as={PaginationButtonContainer}
                    iconAs={PaginationButtonIcon}
                    key={index + 1} 
                    onClick={() => onChange(index + 1)}
                    title={index + 1}
                    $variant={current === index + 1 ? 'primary' : 'secondary'}
                />
            ))}
            <Button
                as={PaginationButtonContainer}
                iconAs={PaginationButtonIcon}
                onClick={() => onChange(current + 1)}
                icon={<MdNavigateNext />}
                disabled={current === pages}
            />
        </PaginationContainer>
    );
}
export default Pagination;