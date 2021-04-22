import io from 'socket.io-client';
import { addResponseMessage, renderCustomComponent } from "react-chat-widget";
import ActionCard from "pages/ActionCard";
import { domain } from 'config';
import CardsList, { ICard } from 'pages/feedlist/CardsList';

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

const socket = io(domain, {
    transports: ['websocket'],
    autoConnect: true
});

const cardInfo = {
    subtext: '',
    image: 'https://dfzximg02.dftoutiao.com/news/20210331/20210331154746_579c8ef07816b5e82889a0a7ce963c76_1_mwpm_03201609.png',
    heading: '沪剧电影《挑山女人》开启长三角巡回演映'
  }  

socket.on('answer', function (data: any) {
    getLiveChatResponse(data)
})

function getLiveChatResponse(data: any) {
    data = JSON.parse(data)
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
    else if (data.msgtype === "feedCard") {
        const cardInfos = {cards: data.feedCard.links.map(link => {
            return {
                messageLink: link.messageURL,
                image: link.picURL,
                heading: link.title
            }
        })}
        renderCustomComponent(CardsList, cardInfos)
    }
    else {
        addResponseMessage("???")
    }
}

// do socket chat
 async function doLiveChat(liveChatRequest: ILiveChatRequest) {
    socket.send(liveChatRequest, (data: any) => {
        if (data) {
            console.log('say a word successfully');
        }
    });
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

export default async function (newMessage: string) {
    console.log(`New message incoming! ${newMessage}`);
    const session_id = socket.id
    const liveChatRequest = getLiveChatRequest(session_id, newMessage)
    await doLiveChat(liveChatRequest)
}

export function join() {
    socket.emit('join room');
}
