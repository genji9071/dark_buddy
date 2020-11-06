import { addResponseMessage } from "react-chat-widget";
import localStorage from "utils/localStorage"
import axios from "axios";
import {domain} from "config"

export interface ILiveChatRequest {
    "chatbotUserId": string,
    "sender_id": string,
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
        "sender_id": session_id,
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
        return data.text.content
    }
    if (data.msgtype === "exception") {
        return data.message
    }
    if (data.msgtype === "markdown") {
        return data.markdown.text
    }
    return "???"
}


export default async function (newMessage: string) {
    console.log(`New message incoming! ${newMessage}`);

    const session_id = localStorage.get("session_id")
    const liveChatRequest = getLiveChatRequest(session_id, newMessage)
    const response = await doLiveChat(liveChatRequest)
    if (response) {
        response.result.forEach((element: any) => {
            addResponseMessage(getLiveChatResponse(element));
        }); 
    }
}