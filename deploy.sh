#!/bin/bash
echo "开始自动部署..."
cd /root/PromptHelp
git pull origin main
echo "代码拉取完成"

# 安装依赖
pip3 install -r requirements.txt -q
echo "依赖安装完成"

# 停止旧进程（如果存在）
if [ -f server.pid ]; then
    kill $(cat server.pid) 2>/dev/null
    rm -f server.pid
fi

# 启动服务
./start.sh
echo "服务已重启"
echo "部署完成!"
