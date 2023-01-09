import redis
import datetime
rdb=redis.StrictRedis(host='localhost', port=6379, db=0)
#in order to read strip data
rdb8=redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
current.rdb=rdb
current.rdb8=rdb8

from clickhouse_driver import Client
chdb = Client(host='IP', database='db', password='password')
current.chdb = chdb

cedar = Client(host='IP', database='db', password='password')
current.cedar = cedar
