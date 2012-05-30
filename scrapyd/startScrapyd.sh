#!/bin/bash

#export PYTHONPATH=$PYTHONPATH
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/

SCRAPY_HOME="/home/scrapyer/scrapy-0-12/"
nohup twistd -ny $SCRAPY_HOME/extras/scrapyd.tac 1>logs/scrapyd.log 2>logs/scrapyd.err &
echo "start scrapyd"
sleep 1
