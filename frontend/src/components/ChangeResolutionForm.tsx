import {ChangeEvent, useState} from "react";
import {DataProcessedByService, ServiceProps} from "../../typings";
import axios, {HttpStatusCode} from "axios";
import getDownloadableURL from "../lib/getDownloadableURL.ts";

const ChangeResolutionForm = ({fileName, fileSize, fileBinaryContent}: ServiceProps) => {
    const [height, setHeight] = useState<string>("")
    const [width, setWidth] = useState<string>("")
    const [imageURL, setImageURL] = useState<string>("")
    const handleHeight = (e: ChangeEvent<HTMLInputElement>)=> {
        setHeight(e.target.value)
    }

    const handleWidth = (e: ChangeEvent<HTMLInputElement>) => {
        setWidth(e.target.value)
    }

    const submitChangeResolutionForm = async() => {
        const { data } = await axios.post<DataProcessedByService>("/service", {
            "name": fileName,
            "size": fileSize,
            "content": Array.from(new Uint8Array(fileBinaryContent as ArrayBuffer)),
            "service": "Change resolution",
            "height": height,
            "width": width,
        })
        if (data.status === HttpStatusCode.Ok) {
            const binaryContent = window.atob(data.content)
            const imageURL = getDownloadableURL(binaryContent, data.mime)
            setImageURL(imageURL)
        } else {
            alert("Failed to end service successfully.")
        }
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
            {imageURL.length > 0 ? (
                <div className="flex items-center justify-center">
                    <a href={imageURL} download
                       className="block bg-blue-400 p-4 rounded-lg text-white font-bold w-1/8 mt-4 transition-transform hover:-translate-y-1 hover:translate-x-1 active:bg-blue-500 text-center">
                        Start download (Click me!)
                    </a>
                </div>
                ) : (
                <div className={"flex justify-center items-center mt-4"}>
                    <button
                        className={"font-bold bg-blue-400 text-white drop-shadow px-4 py-2 rounded-lg text-xl"}
                        onClick={submitChangeResolutionForm}
                    >
                        Go!
                    </button>
                </div>
            )}
        </>
    );
};

export default ChangeResolutionForm;