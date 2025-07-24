import pytest
from app.main import app, url_db
import concurrent.futures

@pytest.fixture
def client():
    app.config['TESTING'] = True
    url_db.clear()
    with app.test_client() as client:
        yield client

def test_shorten_valid_url(client):
    response = client.post('/api/shorten', json={"url": "https://www.google.com"})
    data = response.get_json()
    assert response.status_code == 201
    assert "short_url" in data
    assert data["long_url"] == "https://www.google.com"

def test_redirect_existing_short_id(client):
    res = client.post('/api/shorten', json={"url": "https://example.com"})
    short_url = res.get_json()["short_url"]
    short_id = short_url.rsplit("/", 1)[-1]
    
    redirect_res = client.get(f'/{short_id}', follow_redirects=False)
    assert redirect_res.status_code == 302
    assert redirect_res.headers["Location"] == "https://example.com"

def test_click_count_increment(client):
    res = client.post('/api/shorten', json={"url": "https://github.com"})
    short_id = res.get_json()["short_url"].rsplit("/", 1)[-1]
    
    for _ in range(30):
        client.get(f'/{short_id}')
    
    stats_res = client.get(f'/api/stats/{short_id}')
    assert stats_res.status_code == 200
    assert stats_res.get_json()["clicks"] == 30

@pytest.mark.parametrize("payload", [
    {"url": "not_a_url"},
    {"url": ""},
    {},
])
def test_invalid_url_handling(client, payload):
    response = client.post('/api/shorten', json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_thread_safety_shorten_same_url():
    url = "https://thread-safe-test.com"

    def shorten():
        with app.test_client() as thread_client:
            res = thread_client.post('/api/shorten', json={"url": url})
            assert res.status_code in [200, 201]
            return res.get_json()["short_url"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(shorten) for _ in range(10)]
        results = [f.result() for f in futures]

    assert all(r.startswith("http") for r in results)
    assert len(set(results)) == 1  # Ensure all threads returned the same short URL
