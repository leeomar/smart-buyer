#!/bin/bash

project='crawler'
kill_crawler()
{
    ps -efww | grep scrapyd.runner | grep $project | grep -v grep | cut -c 9-15| xargs kill 2>/dev/null
}

check_crawler()
{
    ps -efww | grep scrapyd.runner | grep $project | grep -v grep
    return $?
}

kill_crawler
sleep 2 
check_crawler
if [ $? -ne 0 ]; then
	echo "spider process stop!"
else
    # send stop signal again to force stop
    kill_crawler
    sleep 3
fi

check_crawler
if [ $? -eq 0 ]; then
    ps -efww | grep scrapyd.runner| grep $project | grep -v grep | cut -c 9-15| xargs kill -9 2>/dev/null
fi
# rm the spider queue info from dbs/crawler.db
# rm -rf ./dbs/crawler.db
