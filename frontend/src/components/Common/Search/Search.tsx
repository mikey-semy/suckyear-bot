import React, { useState } from 'react';
import { SearchTypes } from './Search.types';
import { SearchContainer, SearchInput, ClearButton, SearchIcon } from './Search.styles';
import { MdSearch, MdClose } from 'react-icons/md';

const Search: React.FC<SearchTypes> = ({ value, onChange, placeholder = 'Поиск...' }) => {
    const [localValue, setLocalValue] = useState(value);
    
    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            onChange(value);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newValue = e.target.value;
        setLocalValue(newValue);
        onChange(newValue);
    };

    const handleClear = () => {
        setLocalValue('');
        onChange('');
    };

    return (
        <SearchContainer>
            <SearchIcon>
                <MdSearch />
            </SearchIcon>
            <SearchInput
                type="text"
                value={localValue}
                placeholder={placeholder}
                onChange={handleChange}
                onKeyDown={handleKeyDown}
            />
            {localValue && (
                <ClearButton onClick={handleClear}>
                    <MdClose />
                </ClearButton>
            )}  
        </SearchContainer>
        
    );
};
export default Search;