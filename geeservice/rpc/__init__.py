import requests


EXEC_ROUTE = '/rpc/exec'
EVAL_ROUTE = '/rpc/eval'
CLEAR_ROUTE = '/rpc/clear'
PORT = 5001

def exec_code(code):
    resp = requests.post(f'http://localhost:{PORT}{EXEC_ROUTE}',json={'code':code})
    return resp.json()

def eval_code(code):
    resp = requests.post(f'http://localhost:{PORT}{EVAL_ROUTE}',json={'code':code})
    return resp.json()

def clear_code():
    resp = requests.post(f'http://localhost:{PORT}{CLEAR_ROUTE}')
    return resp.json()