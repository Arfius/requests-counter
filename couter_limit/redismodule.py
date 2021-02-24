import aioredis
import asyncio
import typing

class RedisDB:
    def __init__(self, url):
        self.url = url

    async def __create_entry(self, key:str, max_value:int)-> None: 
        if await self.redis.exists(key) == 0:
            await self.__set_key_value(key, int(max_value))

    async def init(self, tuple_key_threshold:tuple)-> None:
        self.redis = await aioredis.create_redis_pool(self.url)
        [await self.__create_entry(key_value[0], key_value[1]) for key_value in tuple_key_threshold]
         
    async def __set_key_value(self, key:str, value:int)-> int:
         return await self.redis.set(key, value)

    async def decrease(self, key:str)-> int:
        await self.redis.decr(key)
        return await self.status(key)

    async def status(self, key:str)-> int:
        res = await self.redis.get(key)
        return int(res) if res is not None else res

    async def destroy(self, key:str)-> int:
        return await self.redis.delete(key)

    async def close(self)-> None:
        self.redis.close()
        await self.redis.wait_closed()