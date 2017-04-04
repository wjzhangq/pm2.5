#!/bin/bash


#value define
urls=("www.baidu.com" "www.youku.com")
http_code=("200" "301" "302" "404")
count=2
connected=0


echo "now start to check net is on or not!"
echo "bash file in /etc/network/if-down.d/net_restart.sh"
#check net is conneted or not
for ((i=0; i < $count; i++))
do
    url=${urls[$i]}
    result=$(curl -o /dev/null -s -m 10 -w %{http_code} $url)
    echo $result
    echo $i
    for flag in ${http_code}
    do
        if [ $flag = $result ];then
            connected=$(expr $connected + 1)
        fi
    done
done


#if net is down then restart and reboot
if [ $connected -eq 0 ];then
    echo "network is not very well !"
    echo "now restart net !"
    /etc/init.d/networking restart
    /sbin/ifup wlan0
    /sbin/ifup eth0
fi
