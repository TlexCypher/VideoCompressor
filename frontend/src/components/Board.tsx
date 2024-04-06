import {ChangeEvent, useState} from "react";
import {Service} from "../../typings";
import CompressForm from "./CompressForm.tsx";
import ChangeResolutionForm from "./ChangeResolutionForm.tsx";
import ChangeAspectRatioForm from "./ChangeAspectRatioForm.tsx";
import ConvertIntoAudioForm from "./ConvertIntoAudioForm.tsx";
import CreateGifForm from "./CreateGifForm.tsx";

const Board = () => {
    const [selectedService, setSelectedService] = useState<Service | null>(null);
    const handleSelectedService = (e: ChangeEvent<HTMLInputElement>) => {
        setSelectedService(e.target.value as Service)
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
                    selectedService &&
                    selectedService === "Compress" ? <CompressForm/> :
                    selectedService === "Change resolution" ? <ChangeResolutionForm/> :
                    selectedService === "Change aspect ratio" ? <ChangeAspectRatioForm/> :
                    selectedService === "Convert into audio" ? <ConvertIntoAudioForm/> : <CreateGifForm/>
                }
            </div>
        </>
    );
};

export default Board;