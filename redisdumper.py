import csv
import redis
r=redis.Redis(host='127.0.0.1',port='6379')

with open("redis.csv", 'w') as rediscsv:
    writer = csv.writer(rediscsv)
    for i in range(1,100001):
        x=[]
        x.append(i)
        if r.hget(i,"hostname"):
            x.append(r.hget(i,"hostname").decode("utf-8"))
        else:
            x.append('None')
        if r.hget(i,"ipaddr"):
            x.append(r.hget(i,"ipaddr").decode("utf-8"))
        else:
            x.append('None')
        if r.hget(i,"STATUS"):
            x.append(r.hget(i,"STATUS").decode("utf-8"))
        else:
            x.append('None')
        if r.hget(i,"TLS1_3"):
            x.append(r.hget(i,"TLS1_3").decode("utf-8"))
        else:
            x.append('None')
        writer.writerow(x)
