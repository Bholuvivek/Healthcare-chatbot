from flask import Flask, redirect, url_for, request, render_template, jsonify
import requests
import json

app = Flask(__name__, template_folder='Templates')
context_set = ""


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/parse',methods=['POST', 'GET'] )
def extract():
  # text=str(request.form.get('value1'))
  payload = json.dumps({"sender": "Rasa","message": "Hello"})
  headers = {'Content-type': 'application/json', 'Accept':     'text/plain'}
  response = requests.request("POST",   url="http://127.0.0.1:5005/webhooks/rest/webhook", headers=headers, data=payload)
  response=response.json()
  # print(response)
  return jsonify({'data': response})
  # return jsonify(response)

if __name__ == '__main__':
    app.run()
