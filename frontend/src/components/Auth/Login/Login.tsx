import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
    FormLogin, 
    LoginTitle, 
    LoginButton, 
    LoginButtonIcon, 
    ErrorContainer, 
    EmptyContainer 
} from './Login.styles';

import { LoginForm } from './Login.types';
import { login } from './Login.api';
import { Input, Button } from '@/components';
import { useAuth } from '@/contexts'; 

const Login = () => {
    const navigate = useNavigate();
    const { setUser, setToken } = useAuth();
    const [error, setError] = useState('');
    const [formData, setFormData] = useState<LoginForm>({
        username: '',
        password: ''
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        
        try {
            const response = await login({
                username: formData.username,
                password: formData.password
            });
            setUser(response.user);
            setToken(response.access_token);
            navigate('/');
        } catch (err: any) {
            if (err.response?.data?.detail === 'User not found') {
                setError('Пользователь не найден');
            } else {
                setError('Ошибка авторизации');
            }
        }
    };

    return (
            <FormLogin onSubmit={handleSubmit}>
                <LoginTitle>Вход в систему</LoginTitle>
                <Input
                    id="username"
                    type="text"
                    value={formData.username}
                    onChange={(e) => setFormData({...formData, username: e.target.value})}
                    placeholder="Логин"
                    hasError={!!error}
                />
                <Input
                    id="password"
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    placeholder="Пароль"
                    hasError={!!error}
                />
                {
                    error ? (
                        <ErrorContainer>{error}</ErrorContainer>
                    ) : (
                        <EmptyContainer />
                    )
                }
                <Button 
                    as={LoginButton}
                    iconAs={LoginButtonIcon}
                    type="submit" 
                    title="Войти" 
                />
            </FormLogin>
    );
};
export default Login;