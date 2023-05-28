# url_shorter API version 0.1
====
Author: Łukasz Patkowski, lpatkowski@gmail.com


Instalation
====
1. Create & activate python 3 environment
2. Install python libs from requirements.txt
```console
foo@bar:~$ pip install -r requirements.txt
```
3. Migrate DB
```console
foo@bar:~$ ./manage.py migrate
```
4. Create user
```console
foo@bar:~$ ./manage.py createsuperuser
```
5. Create DRF Authorization Token for created user
```console
foo@bar:~$ ./manage.py drf_create_token <user_name>
```

Usage
====
### 1. Create short URL from long URL

```
Endpoint URL: /create/
Method: POST
Headers: Content-Type: application/json
         Authorization: Token <generated_token>
Data(JSON):
    {
        "long_url": "<long_url_address>",
    }
```
Example request:
```console
curl -X POST http://127.0.0.1:8000/create/ -H 'Content-Type: application/json' -H 'Authorization: Token 6a29c3f37f58443981cac67cd94b8feecf3f940f' -d '{"long_url": "https://www.toppr.com/guides/python-guide/examples/python-examples/write-python-hello-world-program/"}'
```
Response HTTP 201 Created:
```json
    {
        "short_url":"http://127.0.0.1:8000/bycHGqQO/"
    }
```
```
Other possible HTTP Response status codes:
- HTTP 400 Bad request
- HTTP 401 Unauthorized
```

### 2. Revert short URL to long URL
```
Endpoint URL: /{hash}/
Method: GET
hash regex: r"[0-9a-zA-Z]{8}"
```
Example request
```console
curl -X GET http://127.0.0.1:8000/bycHGqQO/
```
Response Http 200 OK:
```json
    {
        "long_url":"https://www.toppr.com/guides/python-guide/examples/python-examples/write-python-hello-world-program/"
    }
```
```
Other possible HTTP Response status codes:
- HTTP 404 Not found
```

Running tests
====
```console
foo@bar:~$ ./manage.py test
```

