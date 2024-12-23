export interface PaginationTypes {
    total: number;
    limit: number;
    current: number;
    onChange: (page: number) => void;
}