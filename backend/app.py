from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # すべてのオリジンからのアクセスを許可

@app.route('/')
def hello():
    return 'Hello, CORS!'

if __name__ == '__main__':
    app.run(debug=True)