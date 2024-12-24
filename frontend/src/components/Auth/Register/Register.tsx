import { useState } from 'react';
import { RegisterForm } from './Register.types';
import { register } from './Register.api';
import { 
    FormRegister, 
    RegisterTitle, 
    RegisterButton, 
    RegisterButtonIcon, 
    ErrorContainer, 
    EmptyContainer 
} from './Register.styles';
import { Input, Button } from '@/components';

const Register = () => {
    const [error, setError] = useState('');
    const [formData, setFormData] = useState<RegisterForm>({
        username: '',
        email: '',
        password: ''
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        await register({
            username: formData.username,
            password: formData.password,
            email: formData.email
        });
        
    };

    return (
        <FormRegister onSubmit={handleSubmit}>
            <RegisterTitle>Регистрация нового пользователя</RegisterTitle>
            <Input
                id="username"
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                placeholder="Имя"
                hasError={!!error}
            />
            <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                placeholder="Почта"
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
                as={RegisterButton}
                iconAs={RegisterButtonIcon}
                type="submit" 
                title="Войти"
            />
        </FormRegister>
    );
};
export default Register;