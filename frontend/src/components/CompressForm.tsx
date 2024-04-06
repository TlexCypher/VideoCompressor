import {ChangeEvent, useState} from "react";
import {CompressLevel} from "../../typings";

const CompressForm = () => {
    const [compressLevel, setCompressLevel] = useState<CompressLevel | null>(null)
    const handleCompressLevel = (e: ChangeEvent<HTMLInputElement>) => {
        setCompressLevel(e.target.value as CompressLevel)
    }
    const submitCompressForm = () => {

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
            <div className={"flex justify-center items-center"}>
                <button
                    className={"font-bold bg-blue-400 text-white drop-shadow px-4 py-2 rounded-lg text-xl"}
                    onClick={submitCompressForm}
                >
                    Go!
                </button>
            </div>
        </>
    );
};

export default CompressForm;