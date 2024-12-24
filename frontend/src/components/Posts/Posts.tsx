/**
 * Компонент для отображения списка постов с пагинацией, поиском и сортировкой
 * 
 * @component
 * @example
 * return (
 *   <Posts />
 * )
 */
import React, { useEffect, useState, useMemo, useCallback} from 'react';
import { PostsContainer } from "./Posts.styles";
import { getPosts } from './Posts.api';
import { PostListItem, PostsParams, PostsResponse } from './Posts.types';
import { Post, Loading, Error, Empty, Pagination, Search, Sort } from '@/components';
import debounce from 'lodash/debounce';

const Posts: React.FC = () => {
    /** Список постов */
    const [posts, setPosts] = useState<PostListItem[]>([]);
    
    /** Общее количество постов */
    const [total, setTotal] = useState<number>(0);
    
    /** Текст поиска */
    const [searchValue, setSearchValue] = useState('');
    
    /** Флаг поиска */
    const [isSearching, setIsSearching] = useState(false);

    /** Флаг загрузки данных */
    const [loading, setLoading] = useState<boolean>(true);
    
    /** Текст ошибки */
    const [error, setError] = useState<string | null>(null);
    
    /** Флаг отсутствия постов */
    const [empty, setEmpty] = useState<boolean>(false);

    /** Параметры запроса постов */
    const [params, setParams] = useState<PostsParams>({
        page: 1,
        limit: 10,
        sort: 'created_at',
        order: 'desc'
    });

    /**
     * Загружает посты с сервера
     * @param params - Параметры запроса
     */
    const fetchPostsItems = async (params: PostsParams) => {
        setError(null);
        if (params.search) {
            setIsSearching(true);
        } else {
            setLoading(true);
        }
        try {
            const data: PostsResponse = await getPosts(params);
            setEmpty(data.total === 0);
            setPosts(data.items);
            setTotal(data.total);
        } catch (err: any) {
            const error = err as { message?: string };
            let errorMessage: string = 'Нет связи с сервером';
    
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
    
            setError(`Ошибка при загрузке каталога: ${errorMessage}`);
        } finally {
            setLoading(false);
            setIsSearching(false);
        }
    };

    /**
     * Обработчик поиска
     * @param search - Поисковый запрос
     */
    const handleSearch = useCallback((search: string) => {
        setParams(prev => ({ ...prev, search, page: 1 }));
    }, []);
    
    const debouncedSearch = useMemo(
        () => debounce((value: string) => {
            handleSearch(value);
        }, 500),
        [handleSearch]
    );

    /**
     * Обработчик сортировки
     * @param sort - Поле для сортировки
     */ 
    const handleSort = (sort: 'rating' | 'created_at') => {
        setParams(prev => ({ ...prev, sort }));
    };

    /**
     * Обработчик пагинации
     * @param page - Номер страницы
     */
    const handlePage = (page: number) => {
        setParams(prev => ({ ...prev, page }));
    };
    
    /** 
    * Эффект для обновления параметров поиска при изменении searchValue 
    * Сбрасывает страницу на первую при каждом новом поиске
    */
    useEffect(() => {
        debouncedSearch(searchValue);
        return () => {
            debouncedSearch.cancel();
        };
    }, [searchValue, debouncedSearch]);

    /** 
    * Эффект для загрузки постов при изменении параметров
    */
    useEffect(() => {
        fetchPostsItems(params);
    }, [params]);

    return (
        <PostsContainer>
            <Search
                value={searchValue}
                onChange={setSearchValue}
                placeholder='Поиск по постам'    
            />
            
            <Sort
                onSort={handleSort}
                activeSort={params.sort}
            />

            {loading && !isSearching && <Loading />}
            {isSearching && <Loading/>}
            {error && <Error error={{ message: error }}/>}
            {!loading && !error && empty && <Empty />}
        
            {!isSearching && posts.map(post => (
                <Post
                    key={post.id}
                    post={post}
                />
            ))}

            <Pagination
                total={total ?? 0} 
                limit={params.limit ?? 10}
                current={params.page ?? 1}
                onChange={handlePage}
            />
        </PostsContainer>
    );
} 
export default Posts;