#/bin/sh
cd "$(dirname "$0")"

pfile="twistd.pid"
if [ ! -f $pfile ]; then
    echo "$pfile not found"
    exit 1 
fi

pid=`cat $pfile`
kill $pid
sleep 2
ps -efww | grep $pid | grep -v grep
if [ $? -eq 0 ]; then
    echo "fail stop server, pid[$pid]"
else
    echo "succ stop server, pid[$pid]"
fi

#cd -
