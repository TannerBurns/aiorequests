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

    async def _execute(self, fn: Callable, url: str, *args: list, **kwargs: dict):
        return fn(url, *args, **kwargs)
    
    async def async_get(self, url: str, *args: list, **kwargs: dict):
        [kwargs.update(arg) for arg in args if arg and type(arg) == dict]
        args = [arg for arg in args if arg and type(arg) == list]
        return await self._execute(self.session.get, url, *args, **kwargs)
    
    async def async_post(self, url: str, *args: list, **kwargs: dict):
        [kwargs.update(arg) for arg in args if arg and type(arg) == dict]
        args = [arg for arg in args if arg and type(arg) == list]
        return await self._execute(self.session.post, url, *args, **kwargs)
    
    async def async_put(self, url: str, *args: list, **kwargs: dict):
        [kwargs.update(arg) for arg in args if arg and type(arg) == dict]
        args = [arg for arg in args if arg and type(arg) == list]
        return await self._execute(self.session.put, url, *args, **kwargs)
    
    async def async_delete(self, url: str, *args: list, **kwargs: dict):
        [kwargs.update(arg) for arg in args if arg and type(arg) == dict]
        args = [arg for arg in args if arg and type(arg) == list]
        return await self._execute(self.session.delete, url, *args, **kwargs)

    async def async_head(self, url: str, *args: list, **kwargs: dict):
        [kwargs.update(arg) for arg in args if arg and type(arg) == dict]
        args = [arg for arg in args if arg and type(arg) == list]
        return await self._execute(self.session.head, url, *args, **kwargs)
    
    async def _bulk_get_helper(self, calls: List[Tuple[str, list, dict]]):
        return [ 
            await self.async_get(*argtuple) 
            for index in range(0, len(calls), self.workers) 
            for argtuple in calls[index:index+self.workers]
        ]
    
    async def _bulk_post_helper(self, calls: List[Tuple[str, list, dict]]):
        return [ 
            await self.async_post(*argtuple) 
            for index in range(0, len(calls), self.workers) 
            for argtuple in calls[index:index+self.workers]
        ]

    async def _bulk_put_helper(self, calls: List[Tuple[str, list, dict]]):
        return [ 
            await self.async_put(*argtuple) 
            for index in range(0, len(calls), self.workers) 
            for argtuple in calls[index:index+self.workers]
        ]
    
    async def _bulk_delete_helper(self, calls: List[Tuple[str, list, dict]]):
        return [ 
            await self.async_delete(*argtuple) 
            for index in range(0, len(calls), self.workers) 
            for argtuple in calls[index:index+self.workers]
        ]
    
    async def _bulk_head_helper(self, calls: List[Tuple[str, list, dict]]):
        return [ 
            await self.async_head(*argtuple) 
            for index in range(0, len(calls), self.workers) 
            for argtuple in calls[index:index+self.workers]
        ]
  
    async def async_bulk_requests(self, calls: List[Tuple[str, str, list, dict]]):
        '''async_bulk_requests -- perform all requests and wait for responses

        input -- a list of "calls"
            calls -- Tuple(method{str}, url{str}, args{list}, kwargs{dict})
        output -- response objects
        '''

        bulk_get = [call[1:] for call in calls if call[0].lower() == 'get']
        bulk_post = [call[1:] for call in calls if call[0].lower() == 'post']
        bulk_put = [call[1:] for call in calls if call[0].lower() == 'put']
        bulk_delete = [call[1:] for call in calls if call[0].lower() == 'delete']
        bulk_head = [call[1:] for call in calls if call[0].lower() == 'head']
        responses = []
        if bulk_get:
            responses.extend(await self._bulk_get_helper(bulk_get))
        if bulk_post:
            responses.extend(await self._bulk_post_helper(bulk_post))
        if bulk_put:
            responses.extend(await self._bulk_put_helper(bulk_put))
        if bulk_delete:
            responses.extend(await self._bulk_delete_helper(bulk_delete))
        if bulk_head:
            responses.extend(await self._bulk_post_helper(bulk_head))
        return responses

    def bulk_requests(self, calls: List[Tuple[str, str, list, dict]]):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.async_bulk_requests(calls))
