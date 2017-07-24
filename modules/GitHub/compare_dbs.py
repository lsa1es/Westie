import os
import requests

db_so = open('services.so','r')
r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
repos = requests.get('https://api.github.com/repos/lsa1es/Zabbix-Templates/contents/services')
db_github = []
db_so = []
for x in repos.json():
    db_github.append(x[u'name'])

with open('services.so') as inputfile:
    for line in inputfile:
        db_so.append(line.strip())

matches = set(db_so).intersection(db_github)
for srvs in matches:
    srv_gh = requests.get('https://api.github.com/repos/lsa1es/Zabbix-Templates/contents/services/' + srvs )
    for srv_dw in srv_gh.json():
        dw_url = srv_dw[u'download_url']
        dw_name = srv_dw[u'name']
        dw_gh = requests.get(dw_url)
        open(dw_name , 'wb').write(dw_gh.content)
        
