import {ServiceProps} from "../../typings";
import axios from "axios";

const ConvertIntoAudioForm = ({fileName, fileLength, fileBinaryContent}: ServiceProps) => {
    const submitConvertIntoAudioForm = async() => {
        await axios.post("/convertIntoAudio", {
            "name": fileName,
            "length": fileLength,
            "content": fileBinaryContent,
        })
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