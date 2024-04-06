import {ReactNode} from "react";

type LayoutProps = {
    children: ReactNode
}

type Service = "Compress" | "Change resolution" | "Change aspect ratio" | "Convert into audio" | "Create gif"

type CompressLevel = "low" | "medium" | "high"