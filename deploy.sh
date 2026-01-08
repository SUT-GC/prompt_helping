#!/bin/bash

# 宝塔 WebHook 自动部署脚本
# 用于 GitHub push 到 main 分支时自动部署

set -e

# ==================== 配置 ====================

PROJECT_DIR="/root/PromptHelp"
LOG_FILE="$PROJECT_DIR/deploy.log"
BRANCH="main"
REPO_URL="https://github.com/SUT-GC/prompt_helping.git"

# ==================== 日志函数 ====================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" | tee -a "$LOG_FILE"
}

# ==================== 主流程 ====================

log "========== 开始部署 =========="

# 检查项目目录，不存在则 clone
if [ ! -d "$PROJECT_DIR" ]; then
    log "项目目录不存在，开始克隆..."
    mkdir -p "$(dirname "$PROJECT_DIR")"
    git clone "$REPO_URL" "$PROJECT_DIR"
fi

# 进入项目目录
cd "$PROJECT_DIR" || {
    log_error "无法进入项目目录: $PROJECT_DIR"
    exit 1
}

# 拉取最新代码
log "拉取最新代码..."
git fetch origin
git reset --hard "origin/$BRANCH"

# 停止旧服务
log "停止旧服务..."
if [ -x "$PROJECT_DIR/stop.sh" ]; then
    "$PROJECT_DIR/stop.sh" || true
fi

# 启动新服务
log "启动服务..."
if [ -x "$PROJECT_DIR/start.sh" ]; then
    "$PROJECT_DIR/start.sh"
    log "========== 部署完成 =========="
    exit 0
else
    log_error "start.sh 不存在或不可执行"
    exit 1
fi
