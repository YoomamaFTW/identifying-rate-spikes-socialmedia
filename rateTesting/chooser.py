import asyncio
from .database import Database

db = Database.shared()


async def main(speed, interval):
    await asyncio.sleep(speed * 10)
