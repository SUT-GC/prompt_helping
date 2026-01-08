# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Prompt Studio - 智能提示词工作台，提供多种 Prompt 优化与转换工具。基于 Flask 后端 + 单页前端架构。

## Architecture

- **server.py**: Flask HTTP 代理服务器，处理 CORS，代理 `/v1/*` 到豆包 API，加载并提供 prompts。
- **index.html**: 单页前端应用，侧边栏导航，包含设置页、JSON 转换页、Prompt 优化页。
- **prompts/**: System Prompt 模板目录
  - JSON 转换：`image.txt`, `infographic.txt`, `architecture.txt`
  - Prompt 优化：`optimizer_rtf.txt`, `optimizer_costar.txt`, `optimizer_risen.txt`, `optimizer_crispe.txt`, `optimizer_roses.txt`

## Commands

```bash
# 启动服务（后台，自动创建 venv 并安装依赖）
./start.sh

# 停止服务
./stop.sh

# 手动启动（前台）
python server.py

# 自定义端口
PORT=9000 python server.py
```

默认端口 8088。

## Key Implementation Details

- 前端配置（API Key、模型）存储在 localStorage，通过设置页统一管理
- 使用前检查配置状态，未配置时 Toast 提示并引导跳转设置页
- 侧边栏设置按钮显示绿点表示已配置状态
- Prompt 优化支持 5 种框架：RTF、CO-STAR、RISEN、CRISPE、ROSES
