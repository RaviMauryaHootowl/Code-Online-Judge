from flask import Flask, request
import subprocess
import os
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)

def cCodeRunner(cCode):
  cCodeFile = open(os.path.join("codeFiles", "mycode.c"), "w")
  cCodeFile.write(cCode)
  cCodeFile.close()

  opt = ""
  try:
    opt = subprocess.check_output("cd codeFiles && gcc mycode.c -o mycodec", shell=True)    
    opt = subprocess.check_output("cd codeFiles && ./mycodec < customInput.txt > output.txt", shell=True)               
  except subprocess.CalledProcessError as grepexc:                                                                                                   
    opt = "<COMPILATION ERROR>"
  return opt

def cppCodeRunner(cppCode):
  cppCodeFile = open(os.path.join("codeFiles", "mycode.cpp"), "w")
  cppCodeFile.write(cppCode)
  cppCodeFile.close()

  opt = ""
  try:
    opt = subprocess.check_output("cd codeFiles && g++ mycode.cpp -o mycodecpp", shell=True)    
    opt = subprocess.check_output("cd codeFiles && ./mycodecpp < customInput.txt > output.txt", shell=True)               
  except subprocess.CalledProcessError as grepexc:                                                                                                   
    opt = "<COMPILATION ERROR>"
  
  return opt


def pythonCodeRunner(pyCode):
  pyCodeFile = open(os.path.join("codeFiles", "mycode.py"), "w")
  pyCodeFile.write(pyCode)
  pyCodeFile.close()

  opt = ""
  try:
    opt = subprocess.check_output("cd codeFiles && python3 mycode.py < customInput.txt > output.txt", shell=True)                       
  except subprocess.CalledProcessError as grepexc:                                                                                                   
    opt = "<COMPILATION ERROR>"

  return opt

def cSubmitRunner(cCode):
  cCodeFile = open(os.path.join("codeFiles", "mycode.c"), "w")
  cCodeFile.write(cCode)
  cCodeFile.close()

  opt = ""
  try:
    opt = subprocess.check_output("cd codeFiles && gcc mycode.c -o mycodec", shell=True)    
    opt = subprocess.check_output("cd codeFiles && ./mycodec < input.txt > output.txt", shell=True)                   
  except subprocess.CalledProcessError as grepexc:                                                                                                   
    opt = "<COMPILATION ERROR>"
  
  return opt

def cppSubmitRunner(cppCode):
  cppCodeFile = open(os.path.join("codeFiles", "mycode.cpp"), "w")
  cppCodeFile.write(cppCode)
  cppCodeFile.close()

  opt = ""
  try:
    opt = subprocess.check_output("cd codeFiles && g++ mycode.cpp -o mycodecpp", shell=True)    
    opt = subprocess.check_output("cd codeFiles && ./mycodecpp < input.txt > output.txt", shell=True)                   
  except subprocess.CalledProcessError as grepexc:                                                                                                   
    opt = "<COMPILATION ERROR>"
  
  return opt


def pythonSubmitRunner(pyCode):
  pyCodeFile = open(os.path.join("codeFiles", "mycode.py"), "w")
  pyCodeFile.write(pyCode)
  pyCodeFile.close()

  opt = ""
  try:
    opt = subprocess.check_output("cd codeFiles && python3 mycode.py < input.txt > output.txt", shell=True)                       
  except subprocess.CalledProcessError as grepexc:                                                                                                   
    opt = "<COMPILATION ERROR>"

  return opt


@app.route('/api/submitcode', methods =['POST'])
def codeSubmit():
  lang = request.get_json()['lang']

  opt = ""
  if lang == 'py':
    opt = pythonSubmitRunner(request.get_json()['code'])
  elif lang == 'c':
    opt = cSubmitRunner(request.get_json()['code'])
  elif lang == 'cpp':
    opt = cppSubmitRunner(request.get_json()['code'])

  if opt == "<COMPILATION ERROR>":
    return json.dumps({"status" : "COMPILATION ERROR"})
  print("stdout : " + opt.decode("utf-8"))

  #checking code
  userOutputFile = open(os.path.join("codeFiles", 'output.txt'), mode='r')
  userOutput = userOutputFile.read().strip()
  realOutputFile = open(os.path.join("codeFiles", 'realoutput.txt'), mode='r')
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

  customInputFile = open(os.path.join("codeFiles", "customInput.txt"),"w")
  customInputFile.write(request.get_json()['inputTest'])
  customInputFile.close()

  opt = ""
  if lang == 'py':
    opt = pythonCodeRunner(request.get_json()['code'])
  elif lang == 'c':
    opt = cCodeRunner(request.get_json()['code'])
  elif lang == 'cpp':
    opt = cppCodeRunner(request.get_json()['code'])

  if opt == "<COMPILATION ERROR>":
    return json.dumps({"status" : "COMPILATION ERROR", "output" : ""})
  print("stdout : " + opt.decode("utf-8"))

  #checking code
  userOutputFile = open(os.path.join("codeFiles", 'output.txt'), mode='r')
  userOutput = userOutputFile.read().strip()
  return json.dumps({"status" : "PASSED", "output" : userOutput})

if __name__ == '__main__':
  app.run()