"""#!/usr/bin/python"""
import pymysql
import redis
import datetime
conn = pymysql.connect(host='localhost', user='root',database='numan')
rdb = redis.Redis(host='localhost', port=6379, db=0)
from clickhouse_driver import Client
ch = Client('localhost', database='db')
out = dict(name=['a'], sim=['a'], chss=['a'])

print(datetime.datetime.now(), 'getting exec ch')
rows = ch.execute('SELECT sim FROM hss ')
print(datetime.datetime.now(), 'got exec')   
i = 0
for row in rows:
     i += 1
     out['chss'].append(row[0])
print(datetime.datetime.now(), 'got rows', i)


with conn:
    print(datetime.datetime.now(), 'got conn')
    with conn.cursor() as cursor:
        sql = "SELECT name, sim FROM datacenter  WHERE fetched='T' and error_text is null"
        print(datetime.datetime.now(), 'getting exec', sql)
        cursor.execute(sql)
        print(datetime.datetime.now(), 'got exec', sql)
        i = 0
        for row in cursor.fetchall():
            i += 1
            out['name'].append(row[0])
            out['sim'].append(row[1])
        print(datetime.datetime.now(), 'got rows', i)
        
def chunks(l, n):

    """Yield n number of striped chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

for o in out:
    print(datetime.datetime.now(), 'got', o, len(out[o]))
    key = 'dal/' + o
    tmp = 'tmp__' + key
    rdb.delete(tmp)
    print(datetime.datetime.now(), 'delete', tmp)
    i = 0
    for chunk in chunks(out[o], 100000):
        rdb.sadd(tmp, *chunk)
        i += len(chunk)
        print(datetime.datetime.now(), 'sadd', tmp, i)
    rdb.rename(tmp, key)
    print(datetime.datetime.now(), 'renamed', tmp, key)
rdb.rename('dal/chss', 'chsim/chss')
