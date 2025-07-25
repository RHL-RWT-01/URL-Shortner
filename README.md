# URL Shortener Service

### Architecture
![URL Shortener Demo](/architecture.png)

## My Setup Instructions
Setup Project
```
git clone https://github.com/RHL-RWT-01/URL-Shortner

cd URL-Shortner
```

Create & activate Virtual Environment (optional)
```
python3 -m venv venv

source venv/bin/activate 

```

Install Dependencies
```
pip install -r requirements.txt
```

Run App
```
python -m flask --app app.main run
```

Run Tests
```
PYTHONPATH=. pytest tests/test_basic.py -v
```


## My Approach (Taken help from tips)

- URL Generation: Each long URL is mapped to a unique, randomly generated short ID

- Data Storage: All URLs and metadata (original URL, creation time, click count) are stored in a centralized url_db dictionary.

- Redirection: Accessing a short URL performs a lookup in url_db and redirects to the original URL while incrementing the click count.

- Thread Safety: All read and write operations on shared data structure (url_db) are protected using threading.Lock with customized for write operations to ensure safe concurrent access.

- Testing: Test cases using pytest to validate correctness all endpoints and thread safety

##### AI- Use
- Taken help from chatgpt to write regex and test cases
- Creating custom write lock for thread safety is also suggested by chat gpt


#### Full-filled all the Requirements listed below
### Core Requirements

1. **Shorten URL Endpoint**
   - `POST /api/shorten`
   - Accept a long URL in the request body
   - Return a short code (e.g., "abc123")
   - Store the mapping for later retrieval

2. **Redirect Endpoint**
   - `GET /<short_code>`
   - Redirect to the original URL
   - Return 404 if short code doesn't exist
   - Track each redirect (increment click count)

3. **Analytics Endpoint**
   - `GET /api/stats/<short_code>`
   - Return click count for the short code
   - Return creation timestamp
   - Return the original URL

### Technical Requirements

- URLs must be validated before shortening
- Short codes should be 6 characters (alphanumeric)
- Handle concurrent requests properly
- Include basic error handling
- Write at least 5 tests covering core functionality


