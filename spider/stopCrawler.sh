#!/bin/bash

project='downloader'
kill_downloader()
{
    ps -efww | grep scrapyd.runner | grep $project | grep -v grep | cut -c 9-15| xargs kill 2>/dev/null
}

check_downloader()
{
    ps -efww | grep scrapyd.runner | grep $project | grep -v grep
    return $?
}

kill_downloader
sleep 2 
check_downloader
if [ $? -ne 0 ]; then
	echo "spider process stop!"
else
    # send stop signal again to force stop
    kill_downloader
    sleep 3
fi

check_downloader
if [ $? -eq 0 ]; then
    ps -efww | grep scrapyd.runner| grep $project | grep -v grep | cut -c 9-15| xargs kill -9 2>/dev/null
fi
# rm the spider queue info from dbs/downloader.db
# rm -rf ./dbs/downloader.db
