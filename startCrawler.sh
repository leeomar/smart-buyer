#!/bin/bash

index=1
total_spider_num=1
project='cralwer'
while [ $index -le $total_spider_num ]
do 
    #ip_string=`/sbin/ifconfig|awk "(/[0-9]?[0-9]?[0-9]\.[1-9]?[1-9]?[1-9]\.[0-9]?[0-9]?[0-9]\.[0-9]?[0-9]?[0-9]/) {print}"|cut -d: -f2`
    #ip=${ip_string%% *}
    #prefix=`echo $ip | awk -F"." '{print $4}'`

    ipaddress=`/sbin/ifconfig| grep -A 6 eth1 | grep 'inet addr:' |awk -F':' '{print $2}' | awk -F'.' '{print $4}' | awk '{print $1}'`
    format_seq=`printf "%03d" $index`
    spiderid="$project-$ipaddress-$format_seq"
    echo "start spider[$spiderid]"
    curl http://localhost:6801/schedule.json -d project=crawler -d spider=$spiderid -d jobid=$spiderid 

    if [ $? == 0 ]; then
        echo -e  "start spider[$spiderid]" 
    else
        echo -e "fail start spider[$spiderid]"
    fi
    index=$(($index + 1))
done
