import React from 'react';
import { InputContainer, InputField, InputLabel, ErrorText } from './Input.styles';
import { InputTypes } from './Input.types';

const Input: React.FC<InputTypes> = ({
    id,
    type = "text",
    name,
    value = '',
    placeholder,
    label,
    error,
    disabled = false,
    accept,
    multiple = false,
    onChange,
    hasError = false,
}) => {
  return (
    <InputContainer>
        {label && <InputLabel>{label}</InputLabel>}
        <InputField
            type={type}
            name={name}
            value={type !== 'file' ? value : undefined}
            onChange={onChange}
            placeholder={placeholder}
            disabled={disabled}
            id={id}
            hasError={hasError}
            accept={accept}
            multiple={multiple}
            required
        />
        {error && <ErrorText>{error}</ErrorText>}
    </InputContainer>
  );
};

export default Input;
