from flask import Flask, request
import subprocess
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
  result = subprocess.run(['python', 'mycode.py'], stdout=subprocess.PIPE)
  print(result.stdout)
  return json.dumps({"stdout" : result.stdout.decode("utf-8")})

if __name__ == '__main__':
  app.run()