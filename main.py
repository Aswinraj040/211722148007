import os

import requests
from flask import Flask
from flask_cors import CORS
from flask import request , jsonify
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
CORS(app)

curr_state = []
prev_state = []

@app.route('/numbers/<string:num_id>' ,methods=["GET"])
def numbers(num_id):
    global curr_state , prev_state
    resp = requests.post("http://20.244.56.144/evaluation-service/auth" ,json={"email": f"{os.getenv('email')}","name": f"{os.getenv('name')}","rollNo": f"{os.getenv('rollNo')}","accessCode": f"{os.getenv('accessCode')}","clientID": f"{os.getenv('clientID')}","clientSecret": f"{os.getenv('clientSecret')}"})
    token = resp.json()['access_token']
    window_size = 10
    numbers = []
    if num_id == 'p':
        response = requests.get("http://20.244.56.144/evaluation-service/primes" , headers={
            "Authorization" : f"Bearer {token}"
        })
        numbers = response.json()['numbers']
    elif num_id == 'f':
        response = requests.get("http://20.244.56.144/evaluation-service/fibo", headers={
            "Authorization": f"Bearer {token}"
        })
        numbers = response.json()['numbers']
    elif num_id == 'e':
        response = requests.get("http://20.244.56.144/evaluation-service/even", headers={
            "Authorization": f"Bearer {token}"
        })
        numbers = response.json()['numbers']
    elif num_id == 'r':
        response = requests.get("http://20.244.56.144/evaluation-service/rand", headers={
            "Authorization": f"Bearer {token}"
        })
        numbers = response.json()['numbers']
    print(numbers)
    if  len(numbers) < window_size:
        print("I am inside if")
        avg = 0
        curr_state = numbers
        for i in curr_state:
            avg = i + avg
        avg = avg/len(curr_state)
        responseSend = {}
        responseSend["windowPrevState"] = prev_state
        responseSend["windowCurrState"] = curr_state
        responseSend["numbers"] = numbers
        responseSend["avg"] = avg
    else:
        print("I am inside else")
        curr_state.extend(numbers)
        unique_list = []
        for item in curr_state:
            if item not in unique_list:
                unique_list.append(item)
        print(unique_list)
        curr_state = unique_list
        prev_state = curr_state[:-10]
        print("Previous State")
        print(prev_state)
        curr_state = curr_state[-10:]
        print("Current State")
        print(curr_state)
        avg = 0
        for i in curr_state:
            avg = i + avg
        avg = avg/len(curr_state)
        responseSend = {}
        responseSend["windowPrevState"] = prev_state
        responseSend["windowCurrState"] = curr_state
        responseSend["numbers"] = numbers
        responseSend["avg"] = avg
    return responseSend

if __name__ == "__main__":
    app.run(debug=True , host = '0.0.0.0')