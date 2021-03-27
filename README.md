# url-shortener

URL shortener built with Django Rest Framework. User provides a url and the api returns an alternate URL that will redirect to the original.
I don't know how a URL shortener actually works so this was my attempt to reverse engineer the basic functionality of one.

## There are two endpoints:

### POST - https://shortn-it.herokuapp.com/
Endpoint for creating a new URL. The raw URL is passed in the body of the POST request with the key 'raw'. Example request:
```
{
    "raw": "https://realpython.com/pypi-publish-python-package/#preparing-your-package-for-publication"
}
```
Response:
```
{
    "id": 38,
    "raw": "https://realpython.com/pypi-publish-python-package/#preparing-your-package-for-publication",
    "url_hash": "a65417c4",
    "short": "https://shortn-it.herokuapp.com/a65417c4/"
}
```
Can specify a custom URL (3-8 alphanumeric chars) to use by including it in the request body with the key 'custom'. Example request:
```
{
    "raw": "https://realpython.com/pypi-publish-python-package/#preparing-your-package-for-publication",
    "custom": "custom"
}
```
Response:
```
{
    "id": 40,
    "raw": "https://realpython.com/pypi-publish-python-package/#preparing-your-package-for-publication",
    "url_hash": "custom",
    "short": "https://shortn-it.herokuapp.com/custom/"
}
```
### GET - https://shortn-it.herokuapp.com/<url_hash>/
Endpoint for visiting a created URL. If <url_hash> is in the db, will redirect user to the raw URL associated with that URL hash. For example,
let's say we created the 'custom' url above. Visiting *shortn-it.herokuapp.com/custom/* would redirect the user to the original URL,
*https://realpython.com/pypi-publish-python-package/#preparing-your-package-for-publication*.
