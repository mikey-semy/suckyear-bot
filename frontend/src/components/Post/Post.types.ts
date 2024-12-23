export interface PostTypes {
    post: PostItem;
}

export interface PostItem {
    id: string;
    author: string;
    text: string;
    rating: number;
    created_at: string;
    updated_at: string;
    user: string;
  }
