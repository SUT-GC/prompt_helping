#!/bin/bash

# JSON Prompt Converter 服务停止脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PORT=8088

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# 查找占用端口的进程
PID=$(lsof -t -i :$PORT 2>/dev/null | head -1)

if [ -z "$PID" ]; then
    log_warn "服务未在运行"
    exit 0
fi

# 停止服务
log_info "停止服务 (PID: $PID)..."
kill "$PID" 2>/dev/null

# 等待进程结束（最多 5 秒）
count=0
while [ $count -lt 10 ]; do
    if ! lsof -t -i :$PORT > /dev/null 2>&1; then
        break
    fi
    sleep 0.5
    count=$((count + 1))
done

# 检查是否停止成功
if lsof -t -i :$PORT > /dev/null 2>&1; then
    log_warn "服务未响应，强制终止..."
    lsof -t -i :$PORT | xargs kill -9 2>/dev/null
    sleep 1
fi

log_info "服务已停止"
