#!/bin/bash
cd "$(dirname "$0")"
nohup python3 server.py > server.log 2>&1 &
echo $! > server.pid
echo "Server started with PID $(cat server.pid)"
