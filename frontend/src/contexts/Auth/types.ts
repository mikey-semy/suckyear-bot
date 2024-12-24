export interface AuthContextType {
    user: any;
    token: string;
    setUser: (user: any) => void;
    setToken: (token: string) => void;
}