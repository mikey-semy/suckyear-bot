import api, { handleApiResponse, handleApiError} from '@/api';
import { PostItem } from './Post.types';

export const getPost = (post_id: number): Promise<PostItem> =>
    api.get<PostItem>('/api/v1/posts/' + { post_id })
        .then(handleApiResponse)
        .catch(handleApiError);