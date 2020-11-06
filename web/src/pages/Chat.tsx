import React, { useEffect } from 'react';
import { Widget, addResponseMessage } from 'react-chat-widget';

import 'react-chat-widget/lib/styles.css';
import messageHandler from 'utils/messageHandler';

function ChatApp() {

    useEffect(() => {
        const session_id = "session_id"
        addResponseMessage(session_id);
    }, []);

    return (
        <div className="ChatApp">
        <Widget
            handleNewUserMessage={messageHandler}
        />
        </div>
    );
}

export default ChatApp;
