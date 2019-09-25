from flask import Flask, jsonify
import flask_profiler


app = Flask(__name__)
app.config['DEBUG'] = True

app.config['flask_profiler'] = {
    "enabled": app.config["DEBUG"],
    "storage": {
        "engine": "sqlite"
    },
    "basicAuth": {
        "enabled": True,
        "username": "admin",
        "password": "admin"
    },
    "ignore": [
    "^/static/.*"
    ]

}

@app.route('/api')
def my_microservice():
    return jsonify({'Hello': 'World!'}) 

flask_profiler.init_app(app)

if __name__ == '__main__':
    app.run()