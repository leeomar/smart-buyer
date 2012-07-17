#/bin/sh
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

twistd --python core/server.py
sleep 1
if [ -f "twistd.pid" ]; then
    info "start scheduler[`cat twistd.pid`]"
else
    warn "fail start scheduler"
fi
#cd -
