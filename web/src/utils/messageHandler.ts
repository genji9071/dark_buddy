import localStorage from "utils/localStorage"
import axios from "axios";
import {domain} from "config"
import { io } from 'socket.io-client';
import { addResponseMessage, renderCustomComponent } from "react-chat-widget";
import ActionCard from "pages/ActionCard";

export interface ILiveChatRequest {
    "chatbotUserId": string,
    "senderId": string,
    "text": {
        "content": string,
    },
    "senderNick": string
}

export interface IActionCardRequest {
    "title": string,
    "text": string,
    "btns": [{title: any, actionURL: string}]
}

const socket = io(`ws://0.0.0.0:9000`);


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
        renderCustomComponent(ActionCard, data.actionCard as IActionCardRequest)
    }
    else {
        addResponseMessage("???")
    }
}

async function doLiveChat(liveChatRequest: ILiveChatRequest) {
    const res = await axios.post(
        `${domain}/dark_buddy/chat/push`,
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

socket.on('answer', (data: any) => {
    getLiveChatResponse(data)
})

export default async function (newMessage: string) {
    console.log(`New message incoming! ${newMessage}`);
    // toggleMsgLoader()
    const session_id = localStorage.get("session_id")
    const liveChatRequest = getLiveChatRequest(session_id, newMessage)
    await doLiveChat(liveChatRequest)
}

export function join() {
    socket.emit('join', (session_id: string) => {
      });
}
