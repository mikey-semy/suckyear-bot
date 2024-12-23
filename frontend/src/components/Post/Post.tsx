import React from 'react';
import { PostTypes } from './Post.types';

const Post: React.FC<PostTypes> = ({post}) => {
    return (
        <>
            <p>Автор: {post.author}</p>
            <p>Рейтинг: {post.rating}</p>
            <p>Дата создания: {post.created_at}</p>
            <p>{post.text}</p>
        </>
    );
}
export default Post;