import csv
import redis
r=redis.Redis(host='127.0.0.1',port='6379')

#tls1_3=0
#tls1_2=0
#tls1_1=0
#tls1_0=0
#tls1_3_early=0
hashmap={}
for i in range(1,1000001):
    if r.hget(i,"Country"):
        country=r.hget(i,"Country").decode("utf-8")
        if not country in hashmap:
            hashmap[country]={'TLS1_3':0,'TLS1_2':0,'TLS1_1':0,'TLS1_0':0,'TLS1_3_EARLY':0}
        if r.hget(i,"TLS1_3"):
            hashmap[country]['TLS1_3']=hashmap[country]['TLS1_3']+1
        if r.hget(i,"early"):
            hashmap[country]['TLS1_3_EARLY']=hashmap[country]['TLS1_3_EARLY']+1
        if r.hget(i,"TLS1_2"):
            hashmap[country]['TLS1_2']=hashmap[country]['TLS1_2']+1
        if r.hget(i,"TLS1_1"):
            hashmap[country]['TLS1_1']=hashmap[country]['TLS1_1']+1
        if r.hget(i,"TLS1_0"):
            hashmap[country]['TLS1_0']=hashmap[country]['TLS1_0']+1
for country_data in hashmap:
    print(country_data+" "+str(hashmap[country_data]))
