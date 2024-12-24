export interface InputTypes {
    id: string;
    type?: 'text' | 'password' | 'email' | 'number' | 'url' | 'file';
    name?: string;
    value?: string;
    placeholder?: string;
    label?: string;
    error?: string;
    disabled?: boolean;
    accept?: string;
    multiple?: boolean;
    hasError?: boolean;
    onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
}
