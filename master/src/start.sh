#/bin/sh
twistd --python core/server.py

sleep 1
echo "start server(pid:`cat twistd.pid`)..."
