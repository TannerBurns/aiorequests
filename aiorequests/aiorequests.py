import os
import requests
import asyncio

from typing import Callable

class BaseAsyncioClient(object):
    def __init__(self, workers: int= 16, *args: list, **kwargs: dict):
        self.num_workers = workers
        self.session = requests.Session()
        rqAdapters = requests.adapters.HTTPAdapter(
            pool_connections = workers, 
            pool_maxsize = workers+4, 
            max_retries = 3
        )
        self.session.mount("https://", rqAdapters)
        self.session.mount('http://', rqAdapters)
        self.session.headers.update({
                "Accept-Encoding": "gzip, deflate",
                "User-Agent" : "gzip,  Python Asyncio Requests Client"
        })
        self.basepath = os.path.realpath(os.getcwd())

    async def _execute(self, fn: Callable, *args: list, **kwargs: dict):
        return fn(*args, **kwargs)
    
    async def async_get(self, *args, **kwargs):
        return await self._execute(self.session.get, *args, **kwargs)
    
    async def async_post(self, *args, **kwargs):
        return await self._execute(self.session.post, *args, **kwargs)
    
    async def async_put(self, *args, **kwargs):
        return await self._execute(self.session.put, *args, **kwargs)
    
    async def async_delete(self, *args, **kwargs):
        return await self._execute(self.session.delete, *args, **kwargs)

    async def async_head(self, *args, **kwargs):
        return await self._execute(self.session.head, *args, **kwargs)


class aiorequests(BaseAsyncioClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _run(self, fn: Callable, *args, **kwargs):
        return await fn(*args, **kwargs)

    def get(self, *args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(self._run(self.async_get, *args, **kwargs))
    
    def post(self, *args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(self._run(self.async_post, *args, **kwargs))

    def put(self, *args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(self._run(self.async_put, *args, **kwargs))
 
    def delete(self, *args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(self._run(self.async_delete, *args, **kwargs))
    
    def head(self, *args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(self._run(self.async_head, *args, **kwargs))
  
    async def _aio_executor(self, method: str, args: list):
        if method.lower() == 'get':
            return [
                await async_get(*a) 
                for i in range(0, len(args), self.num_workers) 
                for a in args[i:i+self.num_workers]
            ]
        elif method.lower() == 'post':
            return [
                await async_post(*a) 
                for i in range(0, len(args), self.num_workers) 
                for a in args[i:i+self.num_workers]
            ]
        elif method.lower() == 'put':
            return [
                await async_put(*a) 
                for i in range(0, len(args), self.num_workers) 
                for a in args[i:i+self.num_workers]
            ]
        elif method.lower() == 'delete':
            return [
                await async_delete(*a) 
                for i in range(0, len(args), self.num_workers) 
                for a in args[i:i+self.num_workers]
            ]
        elif method.lower() == 'head':
            return [
                await async_head(*a) 
                for i in range(0, len(args), self.num_workers) 
                for a in args[i:i+self.num_workers]
            ]
        else:
            raise Exception(f'Method "{method}" not supported. Choices: get, post, put, delete, head')

    def bulk_request(self, method: str, args: list):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(self._aio_executor(method, args))