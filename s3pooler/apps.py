import sys
import logging
import asyncio
from threading import Thread
from django.apps import AppConfig


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')

class S3PoolerConfig(AppConfig):
    name = 's3pooler'
    scrapp = None
    main = None
    views = None
    async_ = None

    def ready(self):
        if 'runserver' in sys.argv:
            self.load_tasks()
            self.start()

    def load_tasks(self):
        from .tasks import scrapp_s3, update_raw, update_users
        self.scrapp = scrapp_s3
        self.main = update_raw
        self.views = [update_users]

    def start(self):
            new_loop = asyncio.new_event_loop()
            Thread(target=start_loop, args=(new_loop,)).start()
            self.async_ = async_worker(new_loop)
            asyncio.run_coroutine_threadsafe(self.main_loop(), new_loop)
            asyncio.run_coroutine_threadsafe(self.visions_loop(), new_loop)

    async def main_loop(self):
        async_ = self.async_
        while True:
            before, after = await async_(self.scrapp(5), 3)
            before, after = await async_(self.main(before, after), 1)
            [await async_(view(before, after), 0.5) for view in self.views]

    async def visions_loop(self):
        async_ = self.async_
        while True:
            before, after = await async_(self.main(), 4)
            [await async_(view(before, after), 0.5) for view in self.views]
        
def async_worker(loop):
    async def later_async(function, time=0):
        await asyncio.sleep(time) 
        value =  await asyncio.wrap_future(asyncio.run_coroutine_threadsafe(function, loop))
        return value
    return later_async

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
