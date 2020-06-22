import React, {useState, useEffect} from 'react';
import './CodePage.css';
import AceEditor from 'react-ace';

import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-dracula";

const CodePage = () => {
  const [code, setCode] = useState("");
  const [submitResult, setSubmitResult] = useState("");

  const submitCode = () => {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code })
  };
    fetch('http://localhost:5000/api/code', requestOptions)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      setSubmitResult(data.stdout);
    });
  }

  return (
    <div className="codePage">
      <div className="leftPane">
        <div className="questionSection">
          <div className="questionHeader">Question</div>
          <div className="questionTextArea">
            Write a program to reverse a string. <br/><br/>
            Sample Input : react <br/>
            Sample Output : tcaer
          </div>
        </div>
        <div className="runSection">
          <div className="submitOutput">{submitResult}</div>
          <button className="submitCodeBtn" onClick={submitCode}>Submit Code</button>
        </div>
      </div>
      <div className= "rightPane">
        <AceEditor onChange={(newValue) => setCode(newValue)} value={code} fontSize={20} mode="python" theme="dracula" width="100%div" height="100vh"/>
      </div>
    </div>
  );
}

export default CodePage;
