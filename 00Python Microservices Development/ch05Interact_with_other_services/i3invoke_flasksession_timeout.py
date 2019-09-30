from flask import Flask, jsonify
from requests.exceptions import ReadTimeout
from i1flask_session import setup_connector, get_connector


app = Flask(__name__)
setup_connector(app)


@app.route('/api', methods=['GET', 'POST'])
def my_microservice():
    with get_connector(app) as conn:
        try:
            sub_result = conn.get('http://localhost:5000/api', timeout=2.0).json()
        except ReadTimeout:
            sub_result = {}
    return jsonify({'result': sub_result, 'Hello': '###'})


if __name__ == '__main__':
    app.run(port=5002)