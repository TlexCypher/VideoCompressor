import {LayoutProps} from "../../typings";
import Header from "./Header.tsx";

const Layout = ({children}: LayoutProps) => {
    return (
        <>
            <div
                className={"bg-gradient-to-br from-green-200 to-lime-200 " +
                    "w-full h-full top-0 blur-3xl opacity-70 rounded-md absolute -z-10"}
            />
            <Header/>
            {children}
        </>
    );
};

export default Layout;