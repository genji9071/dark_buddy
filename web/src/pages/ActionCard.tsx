import { Card, Button } from "saltui";
import React from "react";
import { addUserMessage } from "react-chat-widget";
import 'saltui/build/salt-ui.css';

const regex = "dtmd://dingtalkclient/sendMessage?content="

export default (data: any)=> {
    const actionCardInfo = data.actionCard
    const title = actionCardInfo.title
    const text = actionCardInfo.text
    const btns = actionCardInfo.btns
    const buttons: JSX.Element[] = []
    btns.forEach((btn: { title: any; actionURL: string; }) => {
        const btnTitle = btn.title
        if (btn.actionURL.search(regex)) {
            const btnAction = btn.actionURL.substr(regex.length)
            buttons.push(<Button type="minor" size="small" display="inline" onClick={addUserMessage(btnAction)}>${btnTitle}</Button>)
        }
    });

    return (
        <Card locale="zh-cn">
            <Card.Body
              title={title}
              content={text}
            >
              通过完整还原规范，建立相应的前端组件库，可以更好地与设计师、产品经理进行沟通合作。通过完整还原规范，建立相应的前端组件库，可以更好地与设计师、产品经理进行沟通合作。
            </Card.Body>
            <Card.Footer
              actions={buttons} 
              content={<span>已等待3小时</span>}>
            </Card.Footer>
          </Card>
      );
}