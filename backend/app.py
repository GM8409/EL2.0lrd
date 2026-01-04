from flask import Flask
from flask import request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/data')
def index():
    return jsonify(
        {'message': 'Hello, Vue!'}
        )

if __name__ == '__main__':
    app.run(debug=True)