from termcolor import colored
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api')
def my_microservice():
    print('request=', request)
    print(colored('request.environ=', 'red'),request.environ)
    response = jsonify({'Hello': 'World!'})
    print(colored('response=', 'green'), response)
    print(response.data)
    return response

if __name__ == '__main__':
    print('app.url_map=> ',app.url_map)
    app.run()
