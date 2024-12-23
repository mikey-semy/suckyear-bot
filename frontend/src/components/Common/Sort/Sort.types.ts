export interface SortTypes {
    onSort: (sort: 'rating' | 'created_at') => void;
    activeSort?: 'rating' | 'created_at';
}