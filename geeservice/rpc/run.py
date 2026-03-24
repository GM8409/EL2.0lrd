from flask import Flask, request, jsonify
from ..geeFunc.baseTool import admin
from . import EXEC_ROUTE,EVAL_ROUTE,CLEAR_ROUTE,PORT

admin()

shared_namespace = {}

app = Flask(__name__)

@app.route(EXEC_ROUTE,methods=['POST'])
def index():
    try:
        exec(request.json.get('code'), shared_namespace)
        return jsonify({
            'code': 200,
            'msg': 'success'
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': str(e)
        })
        
@app.route(EVAL_ROUTE,methods=['POST'])
def index2():
    try:
        result = eval(request.json.get('code'), shared_namespace)
        return jsonify({
            'code': 200,
            'msg': 'success',
            'result': result
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': str(e)
        })

@app.route(CLEAR_ROUTE,methods=['POST'])
def index3():
    try:
        shared_namespace.clear()
        return jsonify({
            'code': 200,
            'msg': 'success'
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': str(e)
        })
    
if __name__ == '__main__':
    app.run(debug=True,port=PORT)
