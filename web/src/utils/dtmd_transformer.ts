
const regex = "dtmd://dingtalkclient/sendMessage?content="


export default function (uri: string) {

    if (uri.search(regex)) {
        const btnAction = uri.substr(regex.length)
        return `javascript:window.messageHandler("${btnAction}")`
    }

    return uri
}