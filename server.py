from flask import Flask, request
import subprocess
import os
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)

def cppCodeRunner(cppCode):
  cppCodeFile = open("mycode.cpp", "w")
  cppCodeFile.write(cppCode)
  cppCodeFile.close()

  opt = ""
  try:
    opt = subprocess.check_output("g++ mycode.cpp -o mycodecpp", shell=True)    
    opt = subprocess.check_output("./mycodecpp < customInput.txt > output.txt", shell=True)                   
  except subprocess.CalledProcessError as grepexc:                                                                                                   
    opt = "<COMPILATION ERROR>"
  
  return opt


def pythonCodeRunner(pyCode):
  pyCodeFile = open("mycode.py", "w")
  pyCodeFile.write(pyCode)
  pyCodeFile.close()

  opt = ""
  try:
    opt = subprocess.check_output("python3 mycode.py < customInput.txt > output.txt", shell=True)                       
  except subprocess.CalledProcessError as grepexc:                                                                                                   
    opt = "<COMPILATION ERROR>"

  return opt


def cppSubmitRunner(cppCode):
  cppCodeFile = open("mycode.cpp", "w")
  cppCodeFile.write(cppCode)
  cppCodeFile.close()

  opt = ""
  try:
    opt = subprocess.check_output("g++ mycode.cpp -o mycodecpp", shell=True)    
    opt = subprocess.check_output("./mycodecpp < input.txt > output.txt", shell=True)                   
  except subprocess.CalledProcessError as grepexc:                                                                                                   
    opt = "<COMPILATION ERROR>"
  
  return opt


def pythonSubmitRunner(pyCode):
  pyCodeFile = open("mycode.py", "w")
  pyCodeFile.write(pyCode)
  pyCodeFile.close()

  opt = ""
  try:
    opt = subprocess.check_output("python3 mycode.py < input.txt > output.txt", shell=True)                       
  except subprocess.CalledProcessError as grepexc:                                                                                                   
    opt = "<COMPILATION ERROR>"

  return opt


@app.route('/api/submitcode', methods =['POST'])
def codeSubmit():
  lang = request.get_json()['lang']

  opt = ""
  if lang == 'py':
    opt = pythonSubmitRunner(request.get_json()['code'])
  elif lang == 'cpp':
    opt = cppSubmitRunner(request.get_json()['code'])

  if opt == "<COMPILATION ERROR>":
    return json.dumps({"status" : "COMPILATION ERROR"})
  print("stdout : " + opt.decode("utf-8"))

  #checking code
  userOutputFile = open('output.txt', mode='r')
  userOutput = userOutputFile.read().strip()
  realOutputFile = open('realoutput.txt', mode='r')
  realOutput = realOutputFile.read().strip()
  userOutputFile.close()
  realOutputFile.close()
  if userOutput == realOutput:
    print('PASSED!')
    return json.dumps({"status" : "PASSED"})
  else:
    print('FAILED!')
    return json.dumps({"status" : "FAILED"})


@app.route('/api/runcode', methods =['POST'])
def codeRun():
  lang = request.get_json()['lang']

  customInputFile = open("customInput.txt","w")
  customInputFile.write(request.get_json()['inputTest'])
  customInputFile.close()

  opt = ""
  if lang == 'py':
    opt = pythonCodeRunner(request.get_json()['code'])
  elif lang == 'cpp':
    opt = cppCodeRunner(request.get_json()['code'])

  if opt == "<COMPILATION ERROR>":
    return json.dumps({"status" : "COMPILATION ERROR", "output" : ""})
  print("stdout : " + opt.decode("utf-8"))

  #checking code
  userOutputFile = open('output.txt', mode='r')
  userOutput = userOutputFile.read().strip()
  return json.dumps({"status" : "PASSED", "output" : userOutput})

if __name__ == '__main__':
  app.run()