import redis
import unittest
from entpy.storage.redis.redis import RedisStorage
from e2e import IntegrationTestFactory
import socket

host = "redis"
try:
    socket.gethostbyname(host)
except:
    host = "127.0.0.1"


conn = redis.Redis(host=host, port=6379, db=0)


class RedisTest(IntegrationTestFactory):
    def setUp(self):
        super(RedisTest, self).setUp(RedisStorage, conn)

    def test_redis(self):
        self.helper()


if __name__ == "__main__":
    unittest.main()
