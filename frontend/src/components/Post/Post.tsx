import React from 'react';
import { PostTypes } from './Post.types';

const Post: React.FC<PostTypes> = ({post}) => {
    return (
        <div>
            <h1>{post}</h1>
        </div>
    );
}
export default Post;