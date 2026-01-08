# Prompt Studio

智能提示词工作台 - 一站式 Prompt 优化与转换工具。

**在线体验**: https://prompt.nuosheng.cloud

## 功能

| 功能 | 说明 |
|------|------|
| 📝 JSON 转换 | 将自然语言转换为结构化 JSON Prompt |
| ✨ Prompt 优化 | 使用业界主流框架优化粗糙 Prompt |

### JSON 转换支持的类型

- 🎨 图像生成 - 插画、海报、产品图
- 📊 信息图表 - 数据可视化、流程图
- 🏗️ 代码架构 - 系统架构图、微服务拓扑

### Prompt 优化支持的框架

| 框架 | 全称 | 适用场景 |
|------|------|---------|
| RTF | Role-Task-Format | 简单快速，日常任务 |
| CO-STAR | Context-Objective-Style-Tone-Audience-Response | 内容创作、营销文案 |
| RISEN | Role-Instructions-Steps-End goal-Narrowing | 精准控制，复杂任务 |
| CRISPE | Context-Role-Input-Steps-Parameters-Example | 多步骤任务，需要约束 |
| ROSES | Role-Objective-Scenario-Expected Solution-Steps | 战略决策、问题分析 |

## 快速开始

### 1. 获取 API Key

访问 [火山引擎控制台](https://console.volcengine.com/ark)，开通豆包大模型服务，创建 API Key。

### 2. 本地运行

```bash
# 启动服务
./start.sh

# 停止服务
./stop.sh
```

访问 http://localhost:8088

### 3. 使用

1. 进入「设置」页面，配置 API Key
2. 选择功能（JSON 转换 / Prompt 优化）
3. 输入内容，选择模板/框架
4. 点击转换/优化

## 项目结构

```
prompt_helping/
├── server.py           # Flask 后端服务
├── index.html          # 前端页面（侧边栏 + 多功能页）
├── prompts/            # System Prompt 模板
│   ├── image.txt       # 图像生成
│   ├── infographic.txt # 信息图表
│   ├── architecture.txt# 代码架构
│   ├── optimizer_rtf.txt      # RTF 框架
│   ├── optimizer_costar.txt   # CO-STAR 框架
│   ├── optimizer_risen.txt    # RISEN 框架
│   ├── optimizer_crispe.txt   # CRISPE 框架
│   └── optimizer_roses.txt    # ROSES 框架
├── start.sh            # 启动脚本
├── stop.sh             # 停止脚本
└── deploy.sh           # 自动部署脚本
```

## 部署

### Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/prompt_helping;
    index index.html;

    location /v1/ {
        proxy_pass http://127.0.0.1:8088;
        proxy_set_header Host $host;
        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
    }

    location /prompts {
        proxy_pass http://127.0.0.1:8088;
    }

    location /health {
        proxy_pass http://127.0.0.1:8088;
    }
}
```

### 自定义端口

```bash
PORT=9000 python server.py
```

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/prompts` | GET | 获取可用的 prompt 类型 |
| `/prompts/{type}` | GET | 获取指定类型的 system prompt |
| `/v1/chat/completions` | POST | 代理到豆包 API |

## 系统要求

- Python 3.7+
- Flask, flask-cors, requests（通过 `start.sh` 自动安装）

## License

MIT
