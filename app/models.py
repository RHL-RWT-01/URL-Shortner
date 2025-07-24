from app.store import url_db, click_count
from datetime import datetime,timezone

def save_url(short_id: str, long_url: str):
    url_db[short_id] = {
        'long_url': long_url,
        'created_at': datetime.now(timezone.utc),
        'clicks': 0
    }
    

def increment_click_count(short_id: str):
    if short_id in url_db:
        url_db[short_id]['clicks'] += 1
        click_count[short_id] = url_db[short_id]['clicks']
    else:
        raise ValueError("Short ID does not exist in the database.")

def get_stats(short_id: str):
    if short_id in url_db:
        return {
            'short_id': short_id,
            'long_url': url_db[short_id]['long_url'],
            'clicks': url_db[short_id]['clicks'],
            'created_at': url_db[short_id]['created_at'].isoformat()
        }
    else:
        raise ValueError("Short ID does not exist in the database.")