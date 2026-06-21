import requests
r = requests.get('http://127.0.0.1:5000/scenario/1')
print('STATUS', r.status_code)
print(r.text[:2000])
