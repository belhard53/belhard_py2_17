import redis
import os
cache = redis.Redis(host='127.0.0.1', port=6379)
cache.set("qq1", '123')
a = cache.get("qq1")
print(a)
