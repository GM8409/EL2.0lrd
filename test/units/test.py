import requests

resp = requests.post('http://localhost:5000/exec',json={'imgId':'123456'})
print(resp)
