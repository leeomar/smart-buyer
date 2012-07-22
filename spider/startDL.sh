#!/bin/bash

info(){
    echo -e "\033[0;32;1m $(date "+%Y-%m-%d %H:%M:%S") [info]: $1 \033[0m"
}

index=1
total_spider_num=1
project='dl'
ipaddress=`/sbin/ifconfig | grep -A 6 eth1 | grep 'inet addr:' |awk -F':' '{print $2}' | awk -F'.' '{print $4}' | awk '{print $1}'`

while [ $index -le $total_spider_num ]
do 
    spiderid="$project-`printf "%03d" $index`"
    msg=`curl http://localhost:6801/schedule.json -d project=downloader -d spider=$spiderid -d jobid=$spiderid` 
    info "start $spiderid, $msg"

    index=$(($index + 1))
done
