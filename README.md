# Aiorequests

![Python3.7 badge](https://img.shields.io/badge/python-v3.7-blue)

    Async requests library built with asyncio and requests. Ability to bulk async request.


# Example

Normal Usage
```python
from aiorequests import AioRequests
client = AioRequests()
resp = client.session.get('https://www.google.com')
print(resp.status_code)
```

IPython Support
```python
from aiorequests import AioRequests
client = AioRequests()
await resp = client.async_get('https://www.google.com')
print(resp.status_code)
```
