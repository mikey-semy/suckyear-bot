import React, { useEffect, useState } from 'react';
import { 
    FormProfile, 
    ProfileTitle, 
    ProfileButton, 
    ProfileButtonIcon, 
    ErrorContainer, 
    EmptyContainer 
} from './Profile.styles';
import { useAuth } from '@/contexts';
import { Input, Button } from '@/components';
import { ProfileForm } from './Profile.types'; // Предполагается, что у вас есть типы для профиля
import { getUserProfile, updateUserProfile} from './Profile.api';
const Profile: React.FC = () => {
    const { user, token } = useAuth(); // Получаем пользователя и токен из контекста
    const [profileData, setProfileData] = useState<ProfileForm>({
        username: user?.username || '',
        email: user?.email || ''
    });
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const data = await getUserProfile(token);
                setProfileData(data);
            } catch (err) {
                setError('Ошибка при загрузке профиля');
            }
        };

        fetchProfile();
    }, [token]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        try {
            await updateUserProfile(token, profileData);
            alert('Профиль обновлен успешно!');
        } catch (err) {
            setError('Ошибка при обновлении профиля');
        }
        
    };
    return (
        <FormProfile onSubmit={handleSubmit}>
            <ProfileTitle>Профиль</ProfileTitle>
            <Input
                id="username"
                type="text"
                value={profileData.username}
                onChange={(e) => setProfileData({...profileData, username: e.target.value})}
                placeholder="Имя"
                hasError={!!error}
            />
            <Input
                id="email"
                type="email"
                value={profileData.email}
                onChange={(e) => setProfileData({...profileData, email: e.target.value})}
                placeholder="Почта"
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
                as={ProfileButton}
                iconAs={ProfileButtonIcon}
                type="submit" 
                title="Войти"
            />
        </FormProfile>
    );
};
export default Profile;