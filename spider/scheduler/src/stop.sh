#/bin/bash
cd "$(dirname "$0")"

#30:黑 31:红 32:绿 33:黄 34:蓝色 35:紫色 36:深绿 37:白色 
warn(){
    echo -e "\033[0;31;1m $(date "+%Y-%m-%d %H:%M:%S") [warn]: $1 \033[0m"
}

info(){
    echo -e "\033[0;32;1m $(date "+%Y-%m-%d %H:%M:%S") [info]: $1 \033[0m"
}

debug(){
    echo -e "\033[0;30;1m $(date "+%Y-%m-%d %H:%M:%S") [debug]: $1 \033[0m"
}

kill_thread(){
    pid=$1
    force_stop=$2

    ps -efww | grep $pid | grep -v grep
    if [ $? -ne 0 ]; then
        warn "no such thread[$pid]"
        exit 1
    fi

    if $force_stop; then
        info 'force stop thread'
        kill -9 $pid
    else
        kill $pid
    fi

    sleep 2
    ps -efww | grep $pid | grep -v grep
    if [ $? -eq 0 ]; then
        warn "fail stop thread[$pid]"
        exit 1
    else
        info "succ stop thread[$pid]"
        exit 0
    fi
}

usage(){
    debug "Usage: /bin/bash stop.sh [-f]"
}

force_stop=false
while getopts "fh" opt
do
    case $opt in
        f ) force_stop=true;; 
        h ) usage
            exit 0;;
        ? ) warn "illegal option"
            exit 1;;
    esac
done
shift $(($OPTIND - 1))

if [ -f 'twistd.pid' ]; then
    pid=`cat twistd.pid`
    kill_thread $pid $force_stop
else
    warn 'twistd.pid not found'
    exit 0
fi
