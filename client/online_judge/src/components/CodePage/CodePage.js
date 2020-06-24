import React, {useState, useEffect} from 'react';
import './CodePage.css';
import AceEditor from 'react-ace';
import PulseLoader from "react-spinners/PulseLoader";

import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/mode-c_cpp";
import "ace-builds/src-noconflict/theme-dracula";

const CodePage = () => {
  const langList = ['c', 'cpp', 'py', 'java']
  const langNames = {
    "c" : "C",
    "cpp" : "C++ 14",
    "py" : "Python",
    "java" : "Java"
  }
  const aceLangs = {
    "c" : "c",
    "cpp" : "c_cpp",
    "py" : "python",
    "java" : "java"
  }
  const [code, setCode] = useState("");
  const [submitResult, setSubmitResult] = useState("");
  const [inputTest, setInputTest] = useState("");
  const [outputTest, setOutputTest] = useState("");
  const [isRunLoading, setIsRunLoading] = useState(false);
  const [isSubmitLoading, setIsSubmitLoading] = useState(false);
  const [editorLang, setEditorLang] = useState("py");

  const submitCode = async () => {
    setIsSubmitLoading(true);
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, "lang" : editorLang })
    };
    await fetch('http://localhost:5000/api/submitcode', requestOptions)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      switch (data.status) {
        case "PASSED":
          setSubmitResult("✅ AC")
          break;
        case "FAILED":
          setSubmitResult("❌ Wrong Answer")
          break;
        case "COMPILATION ERROR":
          setSubmitResult("❕ Compilation Error")
          break;
        default:
          setSubmitResult("💤 Not Able to Run")
          break;
      }
    });
    setIsSubmitLoading(false);
  }

  useEffect(() => {
    console.log(isRunLoading);
  }, [isRunLoading])

  const runCode = async () => {
    setIsRunLoading(true);
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, inputTest, "lang": editorLang })
    };
    await fetch('http://localhost:5000/api/runcode', requestOptions)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      if(data.status == "COMPILATION ERROR"){
        setOutputTest("Compilation Error!!");
      }else{
        setOutputTest(data.output);
      }
    });
    setIsRunLoading(false);
  }

  const changeLang = (lang) => {
    setEditorLang(lang);
    document.querySelector(".langSelectorContainer").style.display = "none";
    for(let i = 0; i < langList.length; i++){
      document.querySelector(`.${langList[i]}`).className = `lang ${langList[i]}`;
    }
  }

  const openLangSelector = () => {
    document.querySelector(`.${editorLang}`).className = `lang ${editorLang} selectedLang`;
    document.querySelector(".langSelectorContainer").style.display = "flex";
  }

  return (
    <div className="codePage">
      <div className="leftPane">
        <div className="questionSection">
          <div className="questionHeader">Question</div>
          <div className="questionTextArea">
            Write a program to reverse a string.
            <div className="questionInput">
              <div className="questionInputHeader">Sample Input</div>
              <div className="questionSampleInput">kush kaka</div>
            </div>
            <div className="questionOutput">
              <div className="questionOutputHeader">Sample Output</div>
              <div className="questionSampleOutput">akak hsuk</div>
            </div>
          </div>
        </div>
        <div className="runSection">
          <div className="runCodeTestContainer">
            <div className="inputContainer">
              <textarea className="ta" value={inputTest} onChange={(e) => setInputTest(e.target.value)} placeholder="Input" spellCheck={false} id="inputTextArea"></textarea>
            </div>
            
            <div className="outputContainer">
            <textarea className="ta" value={outputTest} placeholder="Output" spellCheck={false} id="outputTextArea"></textarea>
            </div>
          </div>
          <div className="runCodeContainer">
            <div>
              <button className="runCodeBtn" onClick={ () => {runCode();}}>
                {
                  (isRunLoading) ? <PulseLoader
                  size={5}
                  color={"#282A36"}
                /> : "Run"
                }
              </button>
            </div>
            
          </div>
        </div>
      </div>
      <div className= "rightPane">
        
        <div className="editorHeader">
          <span>Code Editor</span>
          <span className="editorLang" onClick={openLangSelector}>{langNames[editorLang]}</span>
          <div className="langSelectorContainer">
            <span className="lang c" onClick={() => changeLang('c')}>C</span>
            <span className="lang cpp" onClick={() => changeLang('cpp')}>C++ 14</span>
            <span className="lang py" onClick={() => changeLang('py')}>Python</span>
            <span className="lang java" onClick={() => changeLang('java')}>Java</span>
          </div>
        </div>
        <AceEditor onChange={(newValue) => setCode(newValue)} value={code} fontSize={20} mode={aceLangs[editorLang]} theme="dracula" width="100%" height="100%"/>
        <div className="submitCodeContainer">
          <div className="submitOutput">{submitResult}</div>
          <button className="submitCodeBtn" onClick={submitCode}>
              {
                (isSubmitLoading) ? <PulseLoader
                size={5}
                color={"#282A36"}
              /> : "Submit Code"
              }
          </button>
        </div>
      </div>
    </div>
  );
}

export default CodePage;
