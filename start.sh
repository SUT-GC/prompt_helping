#!/bin/bash

# JSON Prompt Converter 服务启动脚本
# 用法: ./start.sh [--debug]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
LOG_FILE="$SCRIPT_DIR/server.log"
PORT=8088

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查端口是否已被占用
if lsof -t -i :$PORT > /dev/null 2>&1; then
    log_warn "端口 $PORT 已被占用"
    log_info "如需重启，请先执行 ./stop.sh"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    log_info "创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# 安装依赖
log_info "检查依赖..."
pip install -q -r "$SCRIPT_DIR/requirements.txt"

# 启动服务
log_info "启动服务..."
cd "$SCRIPT_DIR"
nohup "$VENV_DIR/bin/python" server.py > "$LOG_FILE" 2>&1 &

# 等待服务启动（最多 30 秒）
log_info "等待服务启动..."
count=0
while [ $count -lt 30 ]; do
    if lsof -t -i :$PORT > /dev/null 2>&1; then
        log_info "服务启动成功"
        log_info "日志文件: $LOG_FILE"
        log_info "访问地址: http://localhost:$PORT"
        exit 0
    fi
    sleep 1
    count=$((count + 1))
done

log_error "服务启动超时，请查看日志: $LOG_FILE"
exit 1
