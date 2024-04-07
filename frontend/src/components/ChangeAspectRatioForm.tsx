import {ChangeEvent, useState} from "react";
import {ServiceProps} from "../../typings";
import axios from "axios";

const ChangeAspectRatioForm = ({fileName, fileSize, fileBinaryContent}: ServiceProps) => {
    const [heightRatio, setHeightRatio] = useState<string>("");
    const [widthRatio, setWidthRatio] = useState<string>("");
    const handleHeightRatio = (e: ChangeEvent<HTMLInputElement>) => {
        setHeightRatio(e.target.value)
    }
    const handleWidthRatio = (e: ChangeEvent<HTMLInputElement>) => {
        setWidthRatio(e.target.value)
    }
    const submitChangeAspectRatioForm = async() => {
        await axios.post("/service", {
            "name": fileName,
            "size": fileSize,
            "content": Array.from(new Uint8Array(fileBinaryContent as ArrayBuffer)),
            "service": "Change aspect ratio",
            "height_ratio": heightRatio,
            "width_ratio": widthRatio,
        })
    }
    return (
        <>
            <div>
                <p className={"text-center text-xl font-bold mt-4"}>Enter height and width</p>
                <div className={"text-center my-4"}>
                    <input
                        placeholder={"height ratio (e.g 16)"}
                        className={"px-4 py-2 rounded-xl drop-shadow"}
                        value={heightRatio}
                        onChange={handleHeightRatio}
                    />
                </div>
                <div className={"text-center"}>
                    <input
                        placeholder={"width ratio (e.g 9)"}
                        className={"px-4 py-2 rounded-xl drop-shadow"}
                        value={widthRatio}
                        onChange={handleWidthRatio}
                    />
                </div>
            </div>
            <div className={"flex justify-center items-center mt-4"}>
                <button
                    className={"font-bold bg-blue-400 text-white drop-shadow px-4 py-2 rounded-lg text-xl"}
                    onClick={submitChangeAspectRatioForm}
                >
                    Go!
                </button>
            </div>
        </>
    );
};

export default ChangeAspectRatioForm;