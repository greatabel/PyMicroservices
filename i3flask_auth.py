from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def auth():
    print("The raw Authorization header")
    print(request.environ.get("HTTP_AUTHORIZATION", 'is empty'))
    print("Flask's Authorization header")
    print(request.authorization)
    return ""

if __name__ == "__main__":
    app.run()