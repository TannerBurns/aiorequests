import asyncio
import os

from typing import Callable, List, Tuple

import requests


class AioRequests(object):
    def __init__(self, workers: int= 16, *args: list, **kwargs: dict):
        self.workers = workers
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

    def get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)
    
    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.session.put(*args, **kwargs)
 
    def delete(self, *args, **kwargs):
        return self.session.delete(*args, **kwargs)
    
    def head(self, *args, **kwargs):
        return self.session.head(*args, **kwargs)
  
    async def _aio_executor(self, method: str, calls: List[Tuple[list, dict]]):
        if method.lower() == 'get':
            return [
                await self.async_get(*argtuple[0], **argtuple[1]) 
                for index in range(0, len(calls), self.workers) 
                for argtuple in calls[index:index+self.workers]
            ]
        elif method.lower() == 'post':
            return [
                await self.async_post(*argtuple[0], **argtuple[1]) 
                for index in range(0, len(calls), self.workers)
                for argtuple in calls[index:index+self.workers]
            ]
        elif method.lower() == 'put':
            return [
                await self.async_put(*argtuple[0], **argtuple[1]) 
                for index in range(0, len(calls), self.workers) 
                for argtuple in calls[index:index+self.workers]
            ]
        elif method.lower() == 'delete':
            return [
                await self.async_delete(*argtuple[0], **argtuple[1]) 
                for index in range(0, len(calls), self.workers) 
                for argtuple in calls[index:index+self.workers]
            ]
        elif method.lower() == 'head':
            return [
                await self.async_head(*argtuple[0], **argtuple[1]) 
                for index in range(0, len(calls), self.workers) 
                for argtuple in calls[index:index+self.workers]
            ]
        else:
            raise Exception(f'Method "{method}" not supported. Choices: get, post, put, delete, head')

    def bulk_request(self, method: str, calls: List[Tuple[list, dict]]):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(self._aio_executor(method, calls))
