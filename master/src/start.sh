#/bin/sh
twistd --python server.py

sleep 1
echo "start server(pid:`cat twistd.pid`)..."
