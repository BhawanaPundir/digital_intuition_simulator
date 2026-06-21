import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

with app.test_client() as c:
    r = c.post('/api/ai-chat', json={'message':'Someone asked for my photos, what do I do?'})
    print('STATUS', r.status_code)
    print(r.get_data(as_text=True))
