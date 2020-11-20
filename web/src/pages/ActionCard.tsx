import React from "react";
import { addUserMessage } from "react-chat-widget";
import messageHandler, { IActionCardRequest } from "utils/messageHandler";
import dtmd_transformer from "utils/dtmd_transformer"
import { Button } from 'antd';
import ReactMarkdown from "react-markdown";


class ActionCard extends React.Component {
    data: IActionCardRequest

    constructor(props: Readonly<IActionCardRequest>) {
        super(props)
        this.data = {
            "title": props.title,
            "text": props.text,
            "btns": props.btns
        }
    }


    regex = "dtmd://dingtalkclient/sendMessage?content="

    render() {
        const buttons: JSX.Element[] = []
        this.data.btns.forEach((btn: { title: any; actionURL: string; }) => {
            const btnTitle = btn.title
            if (btn.actionURL.search(this.regex)) {
                const btnAction = btn.actionURL.substr(this.regex.length)
                buttons.push(<Button className="actionCardsButton" type="text" block onClick={() => {addUserMessage(decodeURI(btnAction)); messageHandler(decodeURI(btnAction));}}>{btnTitle}</Button>)
            }
        });
    
        return (
            <div className="actionCard">
                <ReactMarkdown 
                    source={this.data.text}
                    transformLinkUri={dtmd_transformer}
                    allowDangerousHtml
                />
                {buttons}
            </div>
          );
    }
}

export default ActionCard