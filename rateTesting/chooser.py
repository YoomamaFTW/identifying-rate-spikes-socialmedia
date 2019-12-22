import asyncio
from .database import Database

db = Database.shared()


async def main(speed, interval):
    await asyncio.sleep(speed * 10)
    while True:
        await asyncio.sleep(interval)
        for x in db.rates:
            if len(x) < 2:
                break
