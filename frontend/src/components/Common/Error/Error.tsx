
import { errorMessages } from './Error.data';
import { ErrorTypes } from './Error.types';
import {
    ErrorContainer,
    ErrorTitle,
    ErrorText,
    ErrorMessage
} from "./Error.styles";

const Error: React.FC<ErrorTypes> = ({ error }) => {
    let errorMessage;

    if (!navigator.onLine) {
        errorMessage = "Пожалуйста, проверьте ваше интернет-соединение.";
    } else {
        errorMessage = errorMessages.description || 
                       (error && (error.statusText || error.message) ? 
                           (error.statusText || error.message) : 
                           "Неизвестная ошибка");
    }

    return (
        <ErrorContainer>
            <ErrorTitle>{errorMessages.icon}</ErrorTitle>
            <ErrorText>{errorMessages.title}</ErrorText>
            <ErrorText>
                <ErrorMessage>
                    {errorMessage}
                </ErrorMessage>
            </ErrorText>
        </ErrorContainer>
    );
};

export default Error;
