import redis
redisDb = redis.Redis(host='127.0.0.1', port=6379, db=4)
redisDb.hset('n1', 'k1', 'v1')
