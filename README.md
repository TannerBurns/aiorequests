# Aiorequests

![Python3.7 badge](https://img.shields.io/badge/python-v3.7-blue)

    Async requests library built with asyncio and requests. Ability to bulk async request.


# Example

Normal Usage
```python
from aiorequests import AioRequests
client = AioRequests()
resp = client.session.get('https://www.google.com')

calls = [
    ('get', 'https://www.google.com', {'headers': {'AcceptEncoding''application/json'}}), ('post', 'https://www.github.com')]
responses = client.bulk_requests(calls)
```

IPython Support
```python
from aiorequests import AioRequests
client = AioRequests()
resp = await client.async_get('https://www.google.com')

calls = [
    ('get', 'https://www.google.com', {'headers': {'AcceptEncoding''application/json'}}), ('post', 'https://www.github.com')]
responses = await client.async_bulk_requests(calls)
```
