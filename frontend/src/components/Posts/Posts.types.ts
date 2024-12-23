export interface PostListItem {
    id: string;
    author: string;
    text: string;
    rating: number;
    created_at: string;
    updated_at: string;
    user: string;
  }

export interface PostsParams {
    page?: number;
    limit?: number;
    search?: string;
    sort?: 'rating' | 'created_at';
    order?: 'asc' | 'desc';
}

export interface PostsResponse {
    items: PostListItem[];
    total: number;
    page: number;
    limit: number;
}