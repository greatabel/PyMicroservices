from flask import Flask, jsonify
from i1flask_session import setup_connector, get_connector


app = Flask(__name__)
setup_connector(app)


@app.route('/api', methods=['GET', 'POST'])
def my_microservice():
    with get_connector(app) as conn:
        sub_result = conn.get('http://localhost:5000/api').json()
    return jsonify({'result': sub_result, 'Hello': '###'})


if __name__ == '__main__':
    app.run(port=5001)