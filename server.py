from flask import Flask, request
import subprocess
import os
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)

@app.route('/api/submitcode', methods =['POST'])
def codeSubmit():
  file1 = open("mycode.py","w")
  file1.write(request.get_json()['code'])
  file1.close()
  print(request.get_json())
  #os.system('python mycode.py < input.txt > output.txt')
  opt = ""
  try:
    opt = subprocess.check_output("python mycode.py < input.txt > output.txt", shell=True)                       
  except subprocess.CalledProcessError as grepexc:                                                                                                   
    opt = "<COMPILATION ERROR>"
  
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
  file1 = open("mycode.py","w")
  file1.write(request.get_json()['code'])
  file1.close()
  print(request.get_json())
  
  customInputFile = open("customInput.txt","w")
  customInputFile.write(request.get_json()['inputTest'])
  customInputFile.close()
  #os.system('python mycode.py < input.txt > output.txt')
  opt = ""
  try:
    opt = subprocess.check_output("python mycode.py < customInput.txt > output.txt", shell=True)                       
  except subprocess.CalledProcessError as grepexc:                                                                                                   
    opt = "<COMPILATION ERROR>"
  
  if opt == "<COMPILATION ERROR>":
    return json.dumps({"status" : "COMPILATION ERROR", "output" : ""})
  print("stdout : " + opt.decode("utf-8"))

  #checking code
  userOutputFile = open('output.txt', mode='r')
  userOutput = userOutputFile.read().strip()
  return json.dumps({"status" : "PASSED", "output" : userOutput})

if __name__ == '__main__':
  app.run()