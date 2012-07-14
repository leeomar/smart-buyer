#/bin/sh

if [ -f twistd.pid ]; then
    pid=`cat twistd.pid`
    echo "stop scrapyd[$pid]"
    kill $pid
    sleep 2
    ps ux | grep $pid | grep -v grep
else
    echo 'no twistd.pid'
fi
