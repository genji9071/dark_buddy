import { addResponseMessage, renderCustomComponent, toggleMsgLoader } from "react-chat-widget";
import localStorage from "utils/localStorage"
import axios from "axios";
import {domain} from "config"
import ActionCard from "pages/ActionCard";

export interface ILiveChatRequest {
    "chatbotUserId": string,
    "senderId": string,
    "text": {
        "content": string,
    },
    "senderNick": string
}

async function doLiveChat(liveChatRequest: ILiveChatRequest) {
    const res = await axios.post(
        `${domain}/dark_buddy/chat`,
      liveChatRequest
    );
    return res.data;
  }

function getLiveChatRequest(session_id: string, newMessage: string) {
    const result = {
        "chatbotUserId": "live_chat_chatbotUserId",
        "senderId": session_id,
        "text": {
            "content": newMessage
        },
        "senderNick": "测试账号001"
    }
    return result
}

function getLiveChatResponse(data: any) {
    console.log(`ready to say! ${JSON.stringify(data)}`);

    if (data.msgtype === "text") {
        addResponseMessage(data.text.content)
    }
    else if (data.msgtype === "exception") {
        addResponseMessage(data.message)
    }
    else if (data.msgtype === "markdown") {
        addResponseMessage(data.markdown.text)
    }
    else if (data.msgtype === "actionCard") {
        renderCustomComponent(ActionCard, data)
    }
    else {
        addResponseMessage("???")
    }
}


export default async function (newMessage: string) {
    console.log(`New message incoming! ${newMessage}`);
    toggleMsgLoader()
    const session_id = localStorage.get("session_id")
    const liveChatRequest = getLiveChatRequest(session_id, newMessage)
    const response = await doLiveChat(liveChatRequest)
    if (response) {
        response.result.forEach((element: any) => {
            toggleMsgLoader()
            getLiveChatResponse(element);
        }); 
    }
}