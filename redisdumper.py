import csv
import redis
r=redis.Redis(host='127.0.0.1',port='6379')

with open("redis.csv", 'w') as rediscsv:
    writer = csv.writer(rediscsv)
    for i in range(1,1000001):
        x=[]
        x.append(i)
        if r.hget(i,"hostname"):
            x.append(r.hget(i,"hostname").decode("utf-8"))
        else:
            x.append('')
        if r.hget(i,"ipaddr"):
            x.append(r.hget(i,"ipaddr").decode("utf-8"))
        else:
            x.append('')
        if r.hget(i,"STATUS"):
            x.append("0x"+r.hget(i,"STATUS").decode("utf-8"))
        else:
            x.append('')
        if r.hget(i,"TLS1_3"):
            x.append(r.hget(i,"TLS1_3").decode("utf-8"))
        else:
            x.append('')
        if r.hget(i,"TLS1_2"):
            x.append(r.hget(i,"TLS1_2").decode("utf-8"))
        else:
            x.append('')
        if r.hget(i,"TLS1_1"):
            x.append(r.hget(i,"TLS1_1").decode("utf-8"))
        else:
            x.append('')
        if r.hget(i,"TLS1_0"):
            x.append(r.hget(i,"TLS1_0").decode("utf-8"))
        else:
            x.append('')

        writer.writerow(x)
