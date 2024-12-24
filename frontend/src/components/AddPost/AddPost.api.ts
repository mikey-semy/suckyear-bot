import api, { handleApiResponse, handleApiError} from '@/api';
import { AddPostTypes } from './AddPost.types';

export const createPost = (postData: AddPostTypes): Promise<AddPostTypes> =>
    api.post<AddPostTypes>('/api/v1/posts/', postData)
        .then(handleApiResponse)
        .catch(handleApiError);