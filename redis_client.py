import redis

redis_client = redis.Redis(
    host='redis-15500.crce207.sa-east-1-2.ec2.cloud.redislabs.com',
    port=15500,
    decode_responses=True,
    username="default",
    password="DxLDGrdaumzlrWE85gbHvhrG2AmUFy2n",
)
