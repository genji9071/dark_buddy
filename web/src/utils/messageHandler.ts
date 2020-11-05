import { addResponseMessage } from "react-chat-widget";

export default async function (newMessage: string) {
    console.log(`New message incoming! ${newMessage}`);
    // Now send the message throught the backend API
    addResponseMessage(newMessage);
}