import api, { handleApiResponse, handleApiError} from '@/api';
import { PostsParams, PostsResponse } from './Posts.types';

export const getPosts = (params: PostsParams): Promise<PostsResponse> =>
    api.get<PostsResponse>('/api/v1/posts/', { params })
        .then(handleApiResponse)
        .catch(handleApiError);