import { addResponseMessage } from "react-chat-widget";
import localStorage from "utils/localStorage"

export default async function (newMessage: string) {
    console.log(`New message incoming! ${newMessage}`);
    // Now send the message throught the backend API
    const session_id = localStorage.get("session_id")
    addResponseMessage(`session_id: ${session_id}, mesaage: ${newMessage}`);
}