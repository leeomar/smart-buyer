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
    debug "Usage: /bin/bash startDL.sh [-n thread-num] [dev]"
}

total_spider_num=1
while getopts "n:h" opt
do
    case $opt in
        n ) total_spider_num=$OPTARG;;
        h ) usage
            exit 0;;
        ? ) warn "illegal option"
            exit 1;;
    esac
done
shift $(($OPTIND - 1))

if [ $# -eq 1 ] && [ $1 == 'dev' ]; then
    project='dl-dev'
else
    project='dl'
fi 

index=1
ipaddress=`/sbin/ifconfig | grep -A 6 eth1 | grep 'inet addr:' |awk -F':' '{print $2}' | awk -F'.' '{print $4}' | awk '{print $1}'`

while [ $index -le $total_spider_num ]
do 
    spiderid="$project-`printf "%03d" $index`"
    msg=`curl http://localhost:6802/schedule.json -d project=downloader -d spider=$spiderid -d jobid=$spiderid` 
    info "start $spiderid, $msg"

    index=$(($index + 1))
done
