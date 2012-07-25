#!/bin/bash

warn(){
    echo -e "\033[0;31;1m $(date "+%Y-%m-%d %H:%M:%S") [warn]: $1 \033[0m"
}

info(){
    echo -e "\033[0;32;1m $(date "+%Y-%m-%d %H:%M:%S") [info]: $1 \033[0m"
}

debug(){
    echo -e "\033[0;33;1m $(date "+%Y-%m-%d %H:%M:%S") [debug]: $1 \033[0m"
}

usage(){
    debug "Usage: /bin/bash startDL.sh [-n thread-num] [-h host] [-p port] [release]"
}

host="127.0.0.1"
port=6802
total_spider_num=1
while getopts "n:h:p:u" opt
do
    case $opt in
        n ) total_spider_num=$OPTARG;;
        h ) host=$OPTARG;;
        p ) port=$OPTARG;;
        u ) usage
            exit 0;;
        ? ) warn "illegal option"
            exit 1;;
    esac
done
shift $(($OPTIND - 1))

if [ $# -eq 1 ] && [ $1 == 'release' ]; then
    project='dl-release'
else
    project='dl-dev'
fi 

index=1
ipaddress=`/sbin/ifconfig | grep -A 6 eth1 | grep 'inet addr:' |awk -F':' '{print $2}' | awk -F'.' '{print $4}' | awk '{print $1}'`

SCRAPYD_URL="http://$host:$port"
while [ $index -le $total_spider_num ]
do 
    spiderid="$project-`printf "%03d" $index`"
    msg=`curl $SCRAPYD_URL/schedule.json -d project=downloader -d spider=$spiderid -d jobid=$spiderid` 
    info "start $spiderid, $msg"

    index=$(($index + 1))
done
