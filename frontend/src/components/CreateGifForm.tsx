import {ChangeEvent, useState} from "react";
import {DataProcessedByService, ServiceProps} from "../../typings";
import axios, {HttpStatusCode} from "axios";
import getDownloadableURL from "../lib/getDownloadableURL.ts";

const CreateGifForm = ({fileName, fileSize, fileBinaryContent}: ServiceProps) => {
    const [startTime, setStartTime] = useState<string>("")
    const [endPosition, setEndPosition] = useState<string>("")
    const [flameRate, setFlameRate] = useState<string>("")
    const [resize, setResize] = useState<string>("")
    const [imageURL, setImageURL] = useState<string>("")

    const handleStartTime = (e: ChangeEvent<HTMLInputElement>) => {
        setStartTime(e.target.value)
    }

    const handleEndPosition = (e: ChangeEvent<HTMLInputElement>) => {
        setEndPosition(e.target.value)
    }

    const handleFlameRate = (e: ChangeEvent<HTMLInputElement>) => {
        setFlameRate(e.target.value)
    }

    const handleResize = (e: ChangeEvent<HTMLInputElement>) => {
        setResize(e.target.value)
    }

    const submitCreateGifForm = async() => {
        const { data } = await axios.post<DataProcessedByService>("/service", {
            "name": fileName,
            "size": fileSize,
            "content": Array.from(new Uint8Array(fileBinaryContent)),
            "service": "Create gif",
            "start_time": startTime,
            "end_position": endPosition,
            "flame_rate": flameRate,
            "resize": resize,
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
                <div className={"flex items-center justify-center mt-4"}>
                    <p className={"mr-6 font-bold drop-shadow"}>Start time</p>
                    <input
                        className={"py-2 px-4 drop-shadow rounded-lg"}
                        placeholder={"e.g 00:00:20"}
                        value={startTime}
                        onChange={handleStartTime}
                    />
                </div>
                <div className={"flex items-center justify-center mt-4"}>
                    <p className={"mr-2 font-bold drop-shadow"}>End position</p>
                    <input
                        className={"py-2 px-4 drop-shadow rounded-lg"}
                        placeholder={"e.g 10"}
                        value={endPosition}
                        onChange={handleEndPosition}
                    />
                </div>
                <div className={"flex items-center justify-center mt-4"}>
                    <p className={"mr-5 font-bold drop-shadow"}>Flame rate</p>
                    <input
                        className={"py-2 px-4 drop-shadow rounded-lg"}
                        placeholder={"e.g 10"}
                        value={flameRate}
                        onChange={handleFlameRate}
                    />
                </div>
                <div className={"flex items-center justify-center mt-4"}>
                    <p className={"mr-12 font-bold drop-shadow"}>Resize</p>
                    <input
                        className={"py-2 px-4 drop-shadow rounded-lg"}
                        placeholder={"e.g 300"}
                        value={resize}
                        onChange={handleResize}
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
                        onClick={submitCreateGifForm}
                    >
                        Go!
                    </button>
                </div>
            )}
        </>
    );
};

export default CreateGifForm;