import React, { useMemo } from 'react';
import { Widget } from 'react-chat-widget';
import localStorage from "utils/localStorage";
import { v4 as uuidv4 } from 'uuid';

import 'react-chat-widget/lib/styles.css';
import messageHandler from 'utils/messageHandler';
import "styles/chat.scss"


// api-reference: https://github.com/Wolox/react-chat-widget

function ChatApp() {

    const session_id = uuidv4()
    useMemo(() => {
        localStorage.set("session_id", session_id)
      }, [session_id])

    return (
        <div className="ChatApp">
        <Widget
            handleNewUserMessage={messageHandler}
            title="Darkbuddy"
            subtitle={`当前会话ID：${session_id}`}
            senderPlaceHolder="请对我说：你好"
        />
        </div>
    )
}

export default ChatApp;
