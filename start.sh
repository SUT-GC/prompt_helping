#!/bin/bash
cd "$(dirname "$0")"

# 使用虚拟环境的 Python
if [ -d "venv" ]; then
    PYTHON="./venv/bin/python"
else
    PYTHON="python3"
fi

nohup $PYTHON server.py > server.log 2>&1 &
echo $! > server.pid
echo "Server started with PID $(cat server.pid)"
