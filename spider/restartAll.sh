#!/bin/bash
cd "$(dirname "$0")"
#30:黑 31:红 32:绿 33:黄 34:蓝色 35:紫色 36:深绿 37:白色 

warn(){
    echo -e "\033[0;31;1m $(date "+%Y-%m-%d %H:%M:%S") [warn]: $1 \033[0m"
}

info(){
    echo -e "\033[0;32;1m $(date "+%Y-%m-%d %H:%M:%S") [info]: $1 \033[0m"
}

debug(){
    echo -e "\033[0;33;1m $(date "+%Y-%m-%d %H:%M:%S") [debug]: $1 \033[0m"
}

check_rc(){
    rc=$1
    cmd=$2
    if [ $rc -ne 0 ]; then
        warn "fail execute $cmd"
        exit 1
    fi
    info $1, $2
}

usage(){
    debug "Usage: /bin/bash $0 [dev]"
}

if [ $# -eq 1 ] && [ $1 == 'dev' ]; then
    dev="dev"
fi

sh stopDL.sh $dev
check_rc $?  "stopDL.sh" $dev 

scrapy deploy

scheduler_home='scheduler/src'
cd $scheduler_home
sh stop.sh
check_rc $? "scheduler stop.sh"

sh start.sh
check_rc $? "scheduler start.sh"
cd -

cd $scheduler_home/tests
python loader.py
cd -

sh startDL.sh $dev
check_rc $? "startDL.sh"
