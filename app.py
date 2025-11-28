from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/healthz')
def healthz():
    return jsonify(status="ok"), 200

@app.route('/')
def home():
    return "Hello, CI/CD World!" Welcome to DevOps...., 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
