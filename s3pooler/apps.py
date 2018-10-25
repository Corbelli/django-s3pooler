import sys
import logging
import asyncio
from threading import Thread
from django.apps import AppConfig
    
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')

class S3PoolerConfig(AppConfig):
    name = 's3pooler'

class Loader():
    name = 's3pooler'
    scrapp = None
    main = None
    visions = None
    async_ = None
    views_update = False


    def load_tasks(self, main, visions):
        from .vilma.updaters import update_json, main_factory, vision_factory
        self.scrapp = update_json
        self.main = main_factory(main)
        self.visions = [vision_factory(vision) for vision in visions] 

    def start(self):
            new_loop = asyncio.new_event_loop()
            Thread(target=start_loop, args=(new_loop,)).start()
            self.async_ = async_worker(new_loop)
            asyncio.run_coroutine_threadsafe(self.main_loop(), new_loop)
            asyncio.run_coroutine_threadsafe(self.visions_loop(), new_loop)

    async def main_loop(self):
        async_ = self.async_
        while True:
            try:
                before, after = await async_(self.scrapp(5), 3)
                before, after = await async_(self.main(before, after), 1)
                [await async_(view(before, after), 0.5) for view in self.visions]
            except Exception:
                logging.exception("message")
                continue    

    async def visions_loop(self):
        from .models import Datetimes
        async_ = self.async_
        while True:
            if self.views_update == True:
                try:
                    timestamp_before = Datetimes.objects.last_timestamp('visions')
                    before, after = await async_(self.main(), 4)
                    [await async_(view(before, after), 0.5) for view in self.visions]
                    timestamp_after = Datetimes.objects.last_timestamp('visions')
                    if timestamp_after == timestamp_before:
                        self.views_update = False
                except Exception:
                    logging.exception("message")
                    continue    
            else:
                await asyncio.sleep(4)

def async_worker(loop):
    async def later_async(function, time=0):
        await asyncio.sleep(time) 
        value =  await asyncio.wrap_future(asyncio.run_coroutine_threadsafe(function, loop))
        return value
    return later_async

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
