# TLSSurvey
### A powerful tool capable of scanning around a million websites in about 48 hours on a single cloud instance (Tested on a quad core AWS EC2 and Azure VM). The results of scanning include the ciphers available for negotiation from TLS versions 1.0 to 1.3 along with the server's ip address stored in local Redis instance.
### You need to have a cloud VM with python3 and Redis installed in order to use this. After the setup is complete:
Populate Redis with a million keys in the follwing format:
HSET <serial no> hostname <domain>
For example:
HSET 1 hostname "google.com"
HSET 2 hostname "yahoo.com"
Now launch driver.sh and capture results from Redis. The genstats script can help you capture some quick stats. Additionally, you can also perform earlydata support checks provided in the repo as an addon.
