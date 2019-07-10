import redis
import os


class RedisClient:

    instance = None

    def __init__(self):
        self.redis = redis.Redis(
            host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=0
        )

    @classmethod
    def load(cls):
        if not cls.instance:
            cls.instance = cls()

        return cls.instance

    def get(self, key):
        value = self.redis.get(key)
        if not value:
            return None
        return value.decode("utf-8")

    def set(self, key, value, expiry_time=None):
        if expiry_time is None:
            return self.redis.set(key, value)
        elif type(expiry_time) == int:
            return self.redis.set(key, value, ex=expiry_time)

    def delete(self, key):
        return self.redis.delete(key)
