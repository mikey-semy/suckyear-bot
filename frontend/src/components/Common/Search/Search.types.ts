export interface SearchTypes {
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
    global?: boolean
}