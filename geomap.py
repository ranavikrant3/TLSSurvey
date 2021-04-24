import redis
import IP2Location as ipdb
r=redis.Redis(host='127.0.0.1',port='6379')
for i in range(1,1000001):
    ipobj=ipdb.IP2Location()
    ipobj.open("IP2LOCATION-LITE-DB1.BIN")
    #print(country)
    try:
        if r.hget(i,"ipaddr"):
            r.hset(i,"Country",ipobj.get_country_long(r.hget(i,"ipaddr").decode("utf-8")))
    except Exception as e:
        r.hset(i,"Country","IPv6")
