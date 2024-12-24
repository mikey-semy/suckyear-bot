import { useNavigate } from "react-router-dom";
import { IoExitOutline } from "react-icons/io5";
import { LogoutButton } from './Logout.styles';
import { useAuth } from '@/contexts';

const Logout: React.FC = () => {
    const navigate = useNavigate();
    const { setUser, setToken } = useAuth();

    const handleLogout = () => {
        localStorage.removeItem('token');
        setUser(null);
        setToken('');
        navigate('/login');
    };

    return (
        <LogoutButton onClick={handleLogout}>
            <IoExitOutline size={20}/>
        </LogoutButton>
    );
};
export default Logout;