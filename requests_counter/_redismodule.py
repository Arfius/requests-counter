import aioredis


class RedisDB:
    def __init__(self, url):
        self.url = url
        self.redis = None

    async def create_entry(self, key: str, max_value: int) -> None:
        if await self.redis.exists(key) == 0:
            await self.redis.set(key, max_value)

    async def setup(self):
        if self.redis is None:
            self.redis = await aioredis.create_redis_pool(self.url)

    async def set_key_value(self, key: str, value: int) -> int:
        if await self.redis.exists(key) != 0:
            await self.redis.set(key, value)
            return await self.status(key)
        else:
            None

    async def decrease(self, key: str) -> int:
        await self.redis.decr(key)
        return await self.status(key)

    async def status(self, key: str) -> int:
        res = await self.redis.get(key)
        return res if res is not None else res

    async def destroy(self, key: str) -> bool:
        if await self.redis.exists(key) != 0:
            await self.redis.delete(key)
            return True
        else:
            return False

    async def close(self) -> None:
        self.redis.close()
        await self.redis.wait_closed()

    async def all_keys(self) -> list:
        return await self.redis.keys("*")
