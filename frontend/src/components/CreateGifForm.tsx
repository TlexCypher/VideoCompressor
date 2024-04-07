import {ChangeEvent, useState} from "react";
import {ServiceProps} from "../../typings";
import axios from "axios";

const CreateGifForm = ({fileName, fileSize, fileBinaryContent}: ServiceProps) => {
    const [startTime, setStartTime] = useState<string>("")
    const [endPosition, setEndPosition] = useState<string>("")
    const [flameRate, setFlameRate] = useState<string>("")
    const [resize, setResize] = useState<string>("")

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
        await axios.post("/service", {
            "name": fileName,
            "size": fileSize,
            "content": Array.from(new Uint8Array(fileBinaryContent)),
            "service": "Create gif",
            "start_time": startTime,
            "end_position": endPosition,
            "flame_rate": flameRate,
            "resize": resize,
        })
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
            <div className={"flex justify-center items-center mt-4"}>
                <button
                    className={"font-bold bg-blue-400 text-white drop-shadow px-4 py-2 rounded-lg text-xl"}
                    onClick={submitCreateGifForm}
                >
                    Go!
                </button>
            </div>
        </>
    );
};

export default CreateGifForm;