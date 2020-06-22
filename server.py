from flask import Flask, request
import subprocess
import os
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)

@app.route('/api/code', methods =['POST'])
def codeRun():
  file1 = open("mycode.py","w")
  file1.write(request.get_json()['code'])
  file1.close()
  print(request.get_json())
  os.system('python mycode.py < input.txt > output.txt')

  #checking code
  userOutputFile = open('output.txt', mode='r')
  userOutput = userOutputFile.read().strip()
  realOutputFile = open('realoutput.txt', mode='r')
  realOutput = realOutputFile.read().strip()
  userOutputFile.close()
  realOutputFile.close()
  if userOutput == realOutput:
    print('PASSED!')
    return json.dumps({"stdout" : "Tests PASSED!"})
  else:
    print('FAILED!')
    return json.dumps({"stdout" : "Tests FAILED!"})

if __name__ == '__main__':
  app.run()