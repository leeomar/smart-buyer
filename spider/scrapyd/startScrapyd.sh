#!/bin/bash

#export PYTHONPATH=$PYTHONPATH
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/

SCRAPY_HOME="/home/newbie/workspace/scrapy/"
nohup twistd -ny $SCRAPY_HOME/extras/scrapyd.tac 1>logs/scrapyd.log 2>logs/scrapyd.err &
sleep 1
if [ -f twistd.pid ]; then
    echo "start scrapyd[`cat twistd.pid`]"
else
    echo "start scrapyd"
fi
