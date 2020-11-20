import React from 'react';
import ReactDOM from 'react-dom';
import * as serviceWorker from './serviceWorker';
import ChatApp from './pages/Chat'
import "./styles/index.scss"
import messageHandler from "utils/messageHandler"

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.register();


const Heading = () => {
  return (
    <div className="heading">
        <Logo />
        <Tagline />
    </div>);
  }

const Logo = () => {
  return (
    <div className="logo">
      Dark Buddy
    </div>
  )
}

const Tagline = () => {
  return (
    <h1 className="tagline">
      想到什么，就做点什么。<br/><br/>
      —— 鲁迅
    </h1>
  )
}

window.messageHandler = messageHandler


// if (process.env.REACT_APP_ENV !== "production") {
//   new VConsole()
// }

function App() {
  return (
    <div className="App">
      <Heading />
      <ChatApp />
    </div>
  );
}





const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);