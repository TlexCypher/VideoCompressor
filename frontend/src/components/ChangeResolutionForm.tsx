import {ChangeEvent, useState} from "react";
import {ServiceProps} from "../../typings";
import axios from "axios";

const ChangeResolutionForm = ({fileName, fileLength, fileBinaryContent}: ServiceProps) => {
    const [height, setHeight] = useState<string>("")
    const [width, setWidth] = useState<string>("")
    const handleHeight = (e: ChangeEvent<HTMLInputElement>)=> {
        setHeight(e.target.value)
    }

    const handleWidth = (e: ChangeEvent<HTMLInputElement>) => {
        setWidth(e.target.value)
    }

    const submitChangeResolutionForm = async() => {
        await axios.post("/changeResolution", {
            "name": fileName,
            "length": fileLength,
            "content": fileBinaryContent,
        })
    }

    return (
        <>
            <div>
                <p className={"text-center text-xl font-bold mt-4"}>Enter height and width</p>
                <div className={"text-center my-4"}>
                    <input
                        placeholder={"height (e.g 1280)"}
                        className={"px-4 py-2 rounded-xl drop-shadow"}
                        value={height}
                        onChange={handleHeight}
                    />
                </div>
                <div className={"text-center"}>
                    <input
                        placeholder={"width (e.g 960)"}
                        className={"px-4 py-2 rounded-xl drop-shadow"}
                        value={width}
                        onChange={handleWidth}
                    />
                </div>
            </div>
            <div className={"flex justify-center items-center mt-4"}>
                <button
                    className={"font-bold bg-blue-400 text-white drop-shadow px-4 py-2 rounded-lg text-xl"}
                    onClick={submitChangeResolutionForm}
                >
                    Go!
                </button>
            </div>
        </>
    );
};

export default ChangeResolutionForm;