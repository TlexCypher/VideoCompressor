const getDownloadableURL = (binaryContent: string, mimeType: string): string => {
    const bytes = new Uint8Array(binaryContent.length);
    for (let i = 0; i < binaryContent.length; i++) {
        bytes[i] = binaryContent.charCodeAt(i);
    }
    return URL.createObjectURL(new Blob([bytes], {type: mimeType}))
}

export default getDownloadableURL;