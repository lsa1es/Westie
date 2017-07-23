#!/bin/sh
#
# Compare database services with github
#
#
services_linux=$(systemctl list-units | grep service | grep -w 'loaded active' |  awk -F. '{print $1}' | grep -v '\\x' | grep -v '@' | grep -v -E "systemd|rhel")


github=$(curl -s https://api.github.com/repos/lsa1es/Zabbix-Templates/contents/services | grep name | awk -F\" '{print $4}')
echo $github > github-services
for x in `cat services.so`
do
    e=$(cat github-services | grep $x | wc -l)
    if [ "$e" -eq "1" ]; then
        srv_get=$(curl -s https://api.github.com/repos/lsa1es/Zabbix-Templates/contents/services/$x | grep download_url | awk -F\" '{print $4}')
        echo "$x esta na sua base de dados. Voce deseja fazer download? (y/n)"
        read $opcao
        if [ "$opcao" == "y" ]; then
            for w in `echo $srv_get`
            do
                wget $w
            done
        fi
        else
        echo "$x nao existe em github"
    fi
done


