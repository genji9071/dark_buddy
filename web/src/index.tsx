import React from 'react';
import ReactDOM from 'react-dom';
import * as serviceWorker from './serviceWorker';
import VConsole from "vconsole";
import ChatApp from './pages/Chat'
import { v4 as uuidv4 } from 'uuid';
import localStorage from "utils/localStorage"

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();


const Navbar = () => {
  const session_id = uuidv4()
  localStorage.set("session_id", session_id)
  return (
    <div className="current_session_id">
      <p>Welcome!</p>
      <p>{session_id}</p>
    </div>
  )
}


if (process.env.REACT_APP_ENV !== "production") {
  new VConsole();
  
}

function App() {
  return (
    <div className="App">
      <Navbar />
      <ChatApp />
    </div>
  );
}





const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);