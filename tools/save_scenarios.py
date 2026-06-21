import requests

print('Fetching scenarios...')
res = requests.get('http://127.0.0.1:5000/api/scenarios')
res.raise_for_status()
data = res.json()
print('Got', len(data), 'scenarios')

print('Saving to admin endpoint...')
r = requests.post('http://127.0.0.1:5000/api/admin/save-scenarios', json=data, headers={'Authorization':'Bearer admin-token-CHANGE'})
print('Status:', r.status_code)
print(r.text)
