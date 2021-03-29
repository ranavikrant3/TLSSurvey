from csv import reader
import redis

r=redis.Redis(host='127.0.0.1',port='6379')
with open('top-100k.csv', mode='r') as dns:
    csv_read = reader(dns)
    for row in csv_read:
        r.hset(row[0],'hostname',row[1])
        
