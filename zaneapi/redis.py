import redis


def create_redis(redis_credentials):
    return redis.Redis(**redis_credentials)
