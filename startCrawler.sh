#!/bin/bash

index=1
total_spider_num=1
project='crawler'
ipaddress=`/sbin/ifconfig | grep -A 6 eth1 | grep 'inet addr:' |awk -F':' '{print $2}' | awk -F'.' '{print $4}' | awk '{print $1}'`

while [ $index -le $total_spider_num ]
do 
    format_seq=`printf "%03d" $index`
    #spiderid="$project-$ipaddress-$format_seq"
    spiderid="$format_seq"
    #echo "start spider[$spiderid]"
    curl http://localhost:6801/schedule.json -d project=crawler -d spider=$spiderid -d jobid=$spiderid 
    index=$(($index + 1))
done
