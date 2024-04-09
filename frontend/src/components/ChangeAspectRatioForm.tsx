import {ChangeEvent, useState} from "react";
import {DataProcessedByService, ServiceProps} from "../../typings";
import axios, {HttpStatusCode} from "axios";
import getDownloadableURL from "../lib/getDownloadableURL.ts";

const ChangeAspectRatioForm = ({fileName, fileSize, fileBinaryContent}: ServiceProps) => {
    const [heightRatio, setHeightRatio] = useState<string>("");
    const [widthRatio, setWidthRatio] = useState<string>("");
    const [imageURL, setImageURL] = useState<string>("")
    const handleHeightRatio = (e: ChangeEvent<HTMLInputElement>) => {
        setHeightRatio(e.target.value)
    }
    const handleWidthRatio = (e: ChangeEvent<HTMLInputElement>) => {
        setWidthRatio(e.target.value)
    }
    const submitChangeAspectRatioForm = async() => {
        const { data } = await axios.post<DataProcessedByService>("/service", {
            "name": fileName,
            "size": fileSize,
            "content": Array.from(new Uint8Array(fileBinaryContent as ArrayBuffer)),
            "service": "Change aspect ratio",
            "height_ratio": heightRatio,
            "width_ratio": widthRatio,
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
                        className={"font-bold bg-blue-400 text-white drop-shadow px-4 py-2 rounded-lg text-xl transition-transform hover:-translate-y-1 hover:translate-x-1 active:bg-blue-500"}
                        onClick={submitChangeAspectRatioForm}
                    >
                        Go!
                    </button>
                </div>
            )}
        </>
    );
};

export default ChangeAspectRatioForm;