import sys
import logging
import asyncio
from threading import Thread

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(message)s')

class Loader():
    scrapp = None
    main = None
    visions = None
    purge = None
    async_ = None
    views_update = False

    def start_pooler(self,  visions):
        from .internal.updaters import update_json, main_factory, vision_factory, purge_jsonevents_table
        self.scrapp = update_json
        self.main = main_factory(visions[0])
        self.visions = [vision_factory(vision) for vision in visions[1:]] 
        self.purge = purge_jsonevents_table
        self.start()

    def start(self):
        if 'runserver' in sys.argv:
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
                before, after = await async_(self.main(1, before, after), 1)
                [await async_(view(i + 2, before, after), 0.5) for (i, view) in enumerate(self.visions)]
                await async_(self.purge())
            except Exception:
                logging.exception("message")
                continue    

    async def visions_loop(self):
        from .models import Datetimes
        async_ = self.async_
        while True:
            if Loader.views_update == True:
                try:
                    timestamp_before = Datetimes.objects.last_timestamp('visions')
                    before, after = await async_(self.main(1), 4)
                    [await async_(view(i + 2, before, after), 0.5) for (i, view) in enumerate(self.visions)]
                    timestamp_after = Datetimes.objects.last_timestamp('visions')
                    if timestamp_after == timestamp_before:
                        Loader.views_update = False
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