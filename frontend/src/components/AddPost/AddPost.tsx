import React, { useState} from 'react';
import { AddPostTypes } from './AddPost.types';
import {createPost} from './AddPost.api';
import { 
    AddPostContainer, 
    AddPostForm, 
    AddPostInput, 
    AddPostTextArea, 
    ErrorMessage, 
    AddPostButton 
} from './AddPost.styles';

const AddPost: React.FC = () => {
    const [loading, setLoading] = useState<boolean>(false);  
    const [error, setError] = useState<string | null>(null);
    const [post, setPost] = useState<AddPostTypes>({
        title: '',
        content: ''
      });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            await createPost(post);
            
        } catch (error) {
            let errorMessage = 'Нет связи с сервером';
            
            if (error instanceof Error) {
                switch(error.message) {
                    case 'Network Error':
                        errorMessage = 'Интернет пропал, проверь подключение';
                        break;
                    case 'Timeout':
                        errorMessage = 'Сервер тормозит, попробуй позже';
                        break;
                    case 'Not Found':
                        errorMessage = 'Данные куда-то делись, уже ищем';
                        break;
                    case 'Server Error':
                        errorMessage = 'Сервер прилёг отдохнуть, скоро встанет';
                        break;
                    default:
                        errorMessage = error.message || 'Неизвестная ошибка';
                }
            }
            setError(errorMessage);
        } finally {
            setLoading(false);
            setPost({ title: '', content: '' });
        }
    };

    return (
        <AddPostContainer>
            <AddPostForm onSubmit={handleSubmit}>
                {error && <ErrorMessage>{error}</ErrorMessage>}
                <AddPostInput
                    type="text"
                    placeholder="Название поста"
                    value={post.title}
                    onChange={(e) => setPost({...post, title: e.target.value})}
                    disabled={loading}
                />
                <AddPostTextArea
                    placeholder="Текст поста"
                    value={post.content}
                    onChange={(e) => setPost({...post, content: e.target.value})}
                    disabled={loading}
                />
                <AddPostButton
                    type="submit"
                    disabled={loading}
                >
                    {loading ? 'Отправляем...' : 'Отправить'}
                </AddPostButton>
            </AddPostForm>
        </AddPostContainer>
    );
}
export default AddPost;