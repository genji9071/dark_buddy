import React, { useEffect } from 'react';
import { Widget, addResponseMessage } from 'react-chat-widget';

import 'react-chat-widget/lib/styles.css';
import messageHandler from 'utils/messageHandler';

function ChatApp() {
  useEffect(() => {
    addResponseMessage('Welcome to this awesome chat!');
  }, []);

  return (
    <div className="App">
      <Widget
        handleNewUserMessage={messageHandler}
      />
    </div>
  );
}

export default ChatApp;
