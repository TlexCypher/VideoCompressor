import {ServiceProps} from "../../typings";
import axios from "axios";

const ConvertIntoAudioForm = ({fileName, fileSize, fileBinaryContent}: ServiceProps) => {
    const submitConvertIntoAudioForm = async() => {
        const { data } = await axios.post("/service", {
            "name": fileName,
            "size": fileSize,
            "content": Array.from(new Uint8Array(fileBinaryContent as ArrayBuffer)),
            "service": "Convert into audio"
        })
        console.log(data)
    }

    return (
        <div className={"flex justify-center items-center mt-4"}>
            <button
                className={"font-bold bg-blue-400 text-white drop-shadow px-4 py-2 rounded-lg text-xl"}
                onClick={submitConvertIntoAudioForm}
            >
                Go!
            </button>
        </div>);
};

export default ConvertIntoAudioForm;