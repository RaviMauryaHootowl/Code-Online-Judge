import React, {useState, useEffect} from 'react';
import './CodePage.css';
import AceEditor from 'react-ace';

import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-dracula";

const CodePage = () => {
  return (
    <div className="codePage">
      <div className="leftPane">
        <div className="questionSection"></div>
        <div className="runSection"></div>
      </div>
      <div className="rightPane">
        <AceEditor fontSize={20} mode="python" theme="dracula" width="100%" height="100vh"/>
      </div>
    </div>
  );
}

export default CodePage;
