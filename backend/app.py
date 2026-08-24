from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hey Folks my AWS 3-Tier Backend is Running Successfully!!!"


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "message": "Backend is working"
    }


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)