import {ChangeEvent, useState} from "react";
import {CompressLevel, ServiceProps, DataProcessedByService} from "../../typings";
import axios, {HttpStatusCode} from 'axios'

const CompressForm = ({fileName, fileSize, fileBinaryContent}: ServiceProps) => {
    const [compressLevel, setCompressLevel] = useState<CompressLevel | null>(null)
    const [imageURL, setImageURL] = useState<string>("")
    const handleCompressLevel = (e: ChangeEvent<HTMLInputElement>) => {
        setCompressLevel(e.target.value as CompressLevel)
    }
    const submitCompressForm = async() => {
        const { data } = await axios.post<DataProcessedByService>("/service", {
            "name": fileName,
            "size": fileSize,
            "content": Array.from(new Uint8Array(fileBinaryContent as ArrayBuffer)),
            "level": compressLevel,
            "service": "Compress"
        })
        if (data.status == HttpStatusCode.Ok) {
            const binaryContent = window.atob(data.content)
            const bytes = new Uint8Array(binaryContent.length);
            for (let i = 0; i < binaryContent.length; i++) {
                bytes[i] = binaryContent.charCodeAt(i);
            }
            const imageURL = URL.createObjectURL(new Blob([bytes], {type: "video/mp4"}))
            setImageURL(imageURL)
        } else {
            alert("Failed to end service successfully.")
        }
    }
    return (
        <>
            <p className={"flex items-center justify-center text-xl drop-shadow font-bold p-4"}>Choose compress level</p>
            <div className={"flex items-center justify-center pb-4"}>
                <div className={"mr-4"}>
                    <input
                        type={"radio"}
                        id={"low"}
                        name={"compress level"}
                        value={"low"}
                        checked={"low" === compressLevel}
                        onChange={handleCompressLevel}
                    />
                    <label htmlFor={"low"} className={"ml-1 font-bold"}>Low</label>
                </div>
                <div className={"mr-4"}>
                    <input
                        type={"radio"}
                        id={"medium"}
                        name={"compress level"}
                        value={"medium"}
                        checked={"medium" === compressLevel}
                        onChange={handleCompressLevel}
                    />
                    <label htmlFor={"medium"} className={"ml-1 font-bold"}>Medium</label>
                </div>
                <div>
                    <input
                        type={"radio"}
                        id={"high"}
                        name={"compress level"}
                        value={"high"}
                        checked={"high" === compressLevel}
                        onChange={handleCompressLevel}
                    />
                    <label htmlFor={"high"} className={"ml-1 font-bold"}>High</label>
                </div>
            </div>
            {imageURL.length > 0 ? (
                <a href={imageURL} download> Start download</a>
            ) : (
                <div className={"flex justify-center items-center"}>
                    <button
                        className={"font-bold bg-blue-400 text-white drop-shadow px-4 py-2 rounded-lg text-xl"}
                        onClick={submitCompressForm}
                    >
                        Go!
                    </button>
                </div>
            )}
        </>
    );
};

export default CompressForm;