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
    const [fileLength, setFileLength] = useState<number>(0)
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
        setFileLength(file.length)
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
                    <p className={"text-center mt-8 drop-shadow font-bold text-2xl"}>
                        Select video!
                    </p>
                    <div className={"flex mt-4 bg-white p-2 rounded-lg w-1/5 mx-auto text-center"}>
                        <input
                            type={"file"}
                            onChange={handleSelectedVideo}
                        />
                    </div>
                    <form>
                        <div className={"flex items-center justify-center space-x-4 mt-4"}>
                            <div>
                                <input
                                    type={"radio"}
                                    id={"Compress"}
                                    name={"service"}
                                    value={"Compress"}
                                    checked={"Compress" === selectedService}
                                    onChange={handleSelectedService}
                                />
                                <label htmlFor={"Compress"} className={"ml-1 font-bold"}>Compress with selected level</label>
                            </div>
                            <div>
                                <input
                                    type={"radio"}
                                    id={"Change resolution"}
                                    name={"service"}
                                    value={"Change resolution"}
                                    checked={"Change resolution" === selectedService}
                                    onChange={handleSelectedService}
                                />
                                <label htmlFor={"Change resolution"} className={"ml-1 font-bold"}>Change resolution</label>
                            </div>
                            <div>
                                <input
                                    type={"radio"}
                                    id={"Change aspect ratio"}
                                    name={"service"}
                                    value={"Change aspect ratio"}
                                    checked={"Change aspect ratio" === selectedService}
                                    onChange={handleSelectedService}
                                />
                                <label htmlFor={"Change aspect ratio"} className={"ml-1 font-bold"}>Change aspect ratio</label>
                            </div>
                            <div>
                                <input
                                    type={"radio"}
                                    id={"Convert into audio"}
                                    name={"service"}
                                    value={"Convert into audio"}
                                    checked={"Convert into audio" === selectedService}
                                    onChange={handleSelectedService}
                                />
                                <label htmlFor={"Convert into audio"} className={"ml-1 font-bold"}>Convert into audio</label>
                            </div>
                            <div>
                                <input
                                    type={"radio"}
                                    id={"Create gif"}
                                    name={"service"}
                                    value={"Create gif"}
                                    checked={"Create gif" === selectedService}
                                    onChange={handleSelectedService}
                                />
                                <label htmlFor={"Create gif"} className={"ml-1 font-bold"}>Create gif</label>
                            </div>
                        </div>
                    </form>
                </div>


                {
                    fileName.length == 0 || !fileBinaryContent ? <NoFileSelected/> :
                    selectedService != null &&
                    selectedService === "Compress" ? <CompressForm fileName={fileName} fileLength={fileLength} fileBinaryContent={fileBinaryContent}/> :
                    selectedService === "Change resolution" ? <ChangeResolutionForm fileName={fileName} fileLength={fileLength} fileBinaryContent={fileBinaryContent}/> :
                    selectedService === "Change aspect ratio" ? <ChangeAspectRatioForm fileName={fileName} fileLength={fileLength} fileBinaryContent={fileBinaryContent}/> :
                    selectedService === "Convert into audio" ? <ConvertIntoAudioForm fileName={fileName} fileLength={fileLength} fileBinaryContent={fileBinaryContent}/> :
                    selectedService === "Create gif" ? <CreateGifForm fileName={fileName} fileLength={fileLength} fileBinaryContent={fileBinaryContent}/> : <></>
                }
            </div>
        </>
    );
};

export default Board;