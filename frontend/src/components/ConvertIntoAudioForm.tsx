import {DataProcessedByService, ServiceProps} from "../../typings";
import axios, {HttpStatusCode} from "axios";
import getDownloadableURL from "../lib/getDownloadableURL.ts";
import {useState} from "react";

const ConvertIntoAudioForm = ({fileName, fileSize, fileBinaryContent}: ServiceProps) => {
    const [imageURL, setImageURL] = useState<string>("")
    const submitConvertIntoAudioForm = async() => {
        const { data } = await axios.post<DataProcessedByService>("/service", {
            "name": fileName,
            "size": fileSize,
            "content": Array.from(new Uint8Array(fileBinaryContent as ArrayBuffer)),
            "service": "Convert into audio"
        })
        if (data.status === HttpStatusCode.Ok) {
            const binaryContent = window.atob(data.content)
            const imageURL = getDownloadableURL(binaryContent, data.mime)
            setImageURL(imageURL)
        } else {
            alert("Failed to end service successfully")
        }
    }

    return (
        <>
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
                        onClick={submitConvertIntoAudioForm}
                    >
                        Go!
                    </button>
                </div>
            )}
        </>
    );
};

export default ConvertIntoAudioForm;