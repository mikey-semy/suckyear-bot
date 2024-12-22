import { useRouteError, /*useNavigate */} from "react-router-dom";
import { Error as ErrorComponent, /*Button*/ } from "@/components";
import { RouteError } from './Error.types';
import { ErrorContainer, /*ErrorButton*/ } from "./Error.styles";

export default function ErrorPage(): JSX.Element {
    const error = useRouteError() as RouteError;
    // const navigate = useNavigate();
    console.error(error);

    return (
        <ErrorContainer>
            <ErrorComponent error={error} />
            {/* <Button
                as={ErrorButton}
                type="button"
                title="Вернуться на главную страницу"
                onClick={() => {
                    navigate("/");
                }}
            /> */}
        </ErrorContainer>
    );
} 