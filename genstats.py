import csv
import redis
r=redis.Redis(host='127.0.0.1',port='6379')

tls1_3=0
tls1_2=0
tls1_1=0
tls1_0=0
tls1_3_early=0

for i in range(1,1000001):
    if r.hget(i,"TLS1_3"):
        tls1_3=tls1_3+1
    if r.hget(i,"early"):
        tls1_3_early=tls1_3_early+1
    if r.hget(i,"TLS1_2"):
        tls1_2=tls1_2+1
    if r.hget(i,"TLS1_1"):
        tls1_1=tls1_1+1
    if r.hget(i,"TLS1_0"):
        tls1_0=tls1_0+1
print("TLS1_3:"+str(tls1_3))
print("TLS1_3_EARLY:"+str(tls1_3_early))
print("TLS1_2:"+str(tls1_2))
print("TLS1_1:"+str(tls1_1))
print("TLS1_0:"+str(tls1_0))
