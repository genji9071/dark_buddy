// eslint-disable-next-line
import React, { useMemo } from 'react';
import { Widget } from 'react-chat-widget';

import 'react-chat-widget/lib/styles.css';
import messageHandler, { join } from 'utils/messageHandler';
import "styles/chat.scss"

// api-reference: https://github.com/Wolox/react-chat-widget

function ChatApp() {

    useMemo(() => {
        join()
      }, [])

    return (
        <div className="ChatApp">
        <Widget
            handleNewUserMessage={messageHandler}
            title="Darkbuddy"
            subtitle="输入 ** 进入菜单"
            senderPlaceHolder="请对我说：你好"
        />
        </div>
    )
}

export default ChatApp;
