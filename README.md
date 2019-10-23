# Aiorequests

![Python3.7 badge](https://img.shields.io/badge/python-v3.7-blue)

    Async requests library built with asyncio and requests. Ability to create single and bulk request.


# Example

Normal Usage
```python
from aiorequests import AioRequests
client = AioRequests()
resp = client.get('https://www.google.com')
print(resp.status_code)
```
```python
from aiorequests import AioRequests
resp = AioRequests().get('https://www.google.com')
print(resp.status_code)
```

IPython Support
```python
from aiorequests import AioRequests
client = AioRequests()
await resp = client.async_get('https://www.google.com')
print(resp.status_code)
```
