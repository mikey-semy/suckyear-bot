import React from 'react';
import { SelectTypes } from './Select.types';
import { SelectContainer, Select as SelectElement, Option, ErrorMessage } from './Select.styles';

const Select: React.FC<SelectTypes> = ({
    id,
    options = [],
    value,
    onChange,
    placeholder,
    disabled,
    error,
    label
}) => {
    return (
        <SelectContainer>
            {label && <label>{label}</label>} 
            <SelectElement
                id={id}
                value={value !== null ? value.toString() : ''}
                onChange={(e) => onChange(e, e.target.value ? Number(e.target.value) : null)}
                disabled={disabled}
                hasError={!!error}
            >
                <Option value="">{placeholder}</Option>
                {options?.map((option) => (
                    <Option key={option.value} value={option.value}>
                        {option.label}
                    </Option>
                ))}
            </SelectElement>
            {error && <ErrorMessage>{error}</ErrorMessage>}
        </SelectContainer>
    );
};

export default Select;