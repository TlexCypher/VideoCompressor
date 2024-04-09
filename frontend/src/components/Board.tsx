import {ChangeEvent, useState} from "react";
import {BinaryFileContent, Service} from "../../typings";
import CompressForm from "./CompressForm.tsx";
import ChangeResolutionForm from "./ChangeResolutionForm.tsx";
import ChangeAspectRatioForm from "./ChangeAspectRatioForm.tsx";
import ConvertIntoAudioForm from "./ConvertIntoAudioForm.tsx";
import CreateGifForm from "./CreateGifForm.tsx";
import NoFileSelected from "./NoFileSelected.tsx";

const Board = () => {
    const [fileName, setFileName] = useState<string>("")
    const [fileSize, setFileSize] = useState<number>(0)
    const [fileBinaryContent, setFileBinaryContent] = useState<BinaryFileContent | null>(null)
    const [selectedService, setSelectedService] = useState<Service>("Compress");
    const handleSelectedService = (e: ChangeEvent<HTMLInputElement>) => {
        setSelectedService(e.target.value as Service)
    }
    const handleSelectedVideo = async(e: ChangeEvent<HTMLInputElement>) => {
        const files = e.currentTarget.files
        if (!files || files?.length === 0) return;
        const file = files[0]
        setFileName(file.name)
        setFileSize(file.size)
        const reader = new FileReader()
        reader.onloadend = () => {
            if(reader.readyState === reader.DONE) {
                const bytes = reader.result as (BinaryFileContent | null)
                setFileBinaryContent(bytes)
            }
        }
        reader.readAsArrayBuffer(file)
    }
    return (
        <>
            <div>
                <div>
                    <p className={"text-center mt-8 drop-shadow font-bold text-3xl"}>
                        Select video!
                    </p>
                    <div className={"flex mt-4 bg-white p-2 rounded-lg w-1/5 mx-auto text-center"}>
                        <input
                            type={"file"}
                            onChange={handleSelectedVideo}
                        />
                    </div>
                    <form className={"flex justify-center"}>
                        <div>
                            <div className={"mt-4 flex items-center"}>
                                <input
                                    className={"h-5 w-5"}
                                    type={"radio"}
                                    id={"Compress"}
                                    name={"service"}
                                    value={"Compress"}
                                    checked={"Compress" === selectedService}
                                    onChange={handleSelectedService}
                                />
                                <label htmlFor={"Compress"} className={"ml-3 font-bold text-3xl drop-shadow"}>Compress with selected level</label>
                            </div>
                            <div className={"mt-4 flex items-center"}>
                                <input
                                    className={"h-5 w-5"}
                                    type={"radio"}
                                    id={"Change resolution"}
                                    name={"service"}
                                    value={"Change resolution"}
                                    checked={"Change resolution" === selectedService}
                                    onChange={handleSelectedService}
                                />
                                <label htmlFor={"Change resolution"} className={"ml-3 font-bold text-3xl drop-shadow"}>Change resolution</label>
                            </div>
                            <div className={"mt-4 flex items-center"}>
                                <input
                                    className={"h-5 w-5"}
                                    type={"radio"}
                                    id={"Change aspect ratio"}
                                    name={"service"}
                                    value={"Change aspect ratio"}
                                    checked={"Change aspect ratio" === selectedService}
                                    onChange={handleSelectedService}
                                />
                                <label htmlFor={"Change aspect ratio"} className={"ml-3 font-bold text-3xl drop-shadow"}>Change aspect ratio</label>
                            </div>
                            <div className={"mt-4 flex items-center"}>
                                <input
                                    className={"h-5 w-5"}
                                    type={"radio"}
                                    id={"Convert into audio"}
                                    name={"service"}
                                    value={"Convert into audio"}
                                    checked={"Convert into audio" === selectedService}
                                    onChange={handleSelectedService}
                                />
                                <label htmlFor={"Convert into audio"} className={"ml-3 font-bold text-3xl drop-shadow"}>Convert into audio</label>
                            </div>
                            <div className={"mt-4 flex items-center"}>
                                <input
                                    className={"h-5 w-5"}
                                    type={"radio"}
                                    id={"Create gif"}
                                    name={"service"}
                                    value={"Create gif"}
                                    checked={"Create gif" === selectedService}
                                    onChange={handleSelectedService}
                                />
                                <label htmlFor={"Create gif"} className={"ml-3 font-bold text-3xl drop-shadow"}>Create gif</label>
                            </div>
                        </div>
                    </form>
                </div>


                {
                    fileName.length == 0 || !fileBinaryContent ? <NoFileSelected/> :
                    selectedService != null &&
                    selectedService === "Compress" ? <CompressForm fileName={fileName} fileSize={fileSize} fileBinaryContent={fileBinaryContent}/> :
                    selectedService === "Change resolution" ? <ChangeResolutionForm fileName={fileName} fileSize={fileSize} fileBinaryContent={fileBinaryContent}/> :
                    selectedService === "Change aspect ratio" ? <ChangeAspectRatioForm fileName={fileName} fileSize={fileSize} fileBinaryContent={fileBinaryContent}/> :
                    selectedService === "Convert into audio" ? <ConvertIntoAudioForm fileName={fileName} fileSize={fileSize} fileBinaryContent={fileBinaryContent}/> :
                    selectedService === "Create gif" ? <CreateGifForm fileName={fileName} fileSize={fileSize} fileBinaryContent={fileBinaryContent}/> : <></>
                }
            </div>
        </>
    );
};

export default Board;