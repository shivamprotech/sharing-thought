import {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';
import {TweetList} from './tweets'

const loadTweets = (callBack) => {
  const xhr = new XMLHttpRequest()
  const method = 'GET'
  const url = 'http://localhost:8000/api/tweets/'
  const responseType = 'json'
  xhr.responseType = responseType
  xhr.open(method, url)
  xhr.onload = () => {
    callBack(xhr.response, xhr.status)
  }
  xhr.send()
}

function App() {
  const [tweets, setTweets] = useState([])

  useEffect(() => {
    const callBack = (response, status) => {
      if (status === 200) {
        setTweets(response)
      }
    }
    loadTweets(callBack)
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <TweetList tweets={tweets}/>

        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
