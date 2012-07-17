#!/bin/bash

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

#SCRAPY_HOME="/home/newbie/workspace/scrapy/"
SCRAPY_HOME="/home/scrapyer/scrapy-0-12/"
nohup twistd -ny $SCRAPY_HOME/extras/scrapyd.tac 1>logs/scrapyd.log 2>logs/scrapyd.err &
sleep 1
if [ -f "twistd.pid" ]; then
    info "start scrapyd[`cat twistd.pid`]"
else
    warn "fail start scrapyd"
fi
