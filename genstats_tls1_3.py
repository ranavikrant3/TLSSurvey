import redis
r=redis.Redis(host='127.0.0.1',port='6379')

count_per_cipher={}
no_implemented={0:0,1:0,2:0,3:0,4:0,5:0}
only_tls1_3=0
tls1_3_1_2=0
all_tls=0
mozilla=0

for seq in range(1,1000001):
    if r.hget(seq,"TLS1_3"):
        TLS1_2=False
        TLS1_1=False
        TLS1_0=False
        if r.hget(seq,"TLS1_2"):
            TLS1_2=True
        if r.hget(seq,"TLS1_1"):
            TLS1_1=True
        if r.hget(seq,"TLS1_0"):
            TLS1_0=True
        if TLS1_0 and TLS1_1 and TLS1_2:
            all_tls=all_tls+1
        if not TLS1_0 and not TLS1_1 and TLS1_2:
            tls1_3_1_2=tls1_3_1_2+1
        if not TLS1_0 and not TLS1_1 and not TLS1_2:
            only_tls1_3=only_tls1_3+1

        tls1_3_ciphers=r.hget(seq,"TLS1_3").decode("utf-8").split(' ')[:-1]
        no_implemented[len(tls1_3_ciphers)]=no_implemented[len(tls1_3_ciphers)]+1
        for cipher in tls1_3_ciphers:
            if cipher not in count_per_cipher:
                count_per_cipher[cipher]=0
            count_per_cipher[cipher]=count_per_cipher[cipher]+1

        if r.hget(seq,"TLS1_3").decode("utf-8")=="TLS_CHACHA20_POLY1305_SHA256 TLS_AES_256_GCM_SHA384 TLS_AES_128_GCM_SHA256 ":
            mozilla=mozilla+1

print("Number of domains with Mozilla Recommended TLS1.3 Ciphers: "+str(mozilla))
print("Number of domains with All TLS Versions Enabled: "+str(all_tls))
print("Number of domains with Only TLS1.3 Enabled: "+str(only_tls1_3))
print("Number of domains with Only TLS1.2 and TLS1.3 Enabled: "+str(tls1_3_1_2))
print("Number of TLS1.3 Ciphers Enabled by the domains: "+str(no_implemented))
print("Frequency of TLS1.3 Ciphers across all the domains: "+str(count_per_cipher))
