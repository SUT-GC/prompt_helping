# JSON Prompt Converter

将自然语言提示词智能转换为结构化 JSON Prompting 的工具。

**在线体验**: https://prompt.nuosheng.cloud

## 使用教程

### 第一步：获取 API Key

1. 访问 [火山引擎控制台](https://console.volcengine.com/ark)
2. 开通豆包大模型服务
3. 创建 API Key 并复制保存

### 第二步：打开工具

访问 https://prompt.nuosheng.cloud

### 第三步：配置 API Key

1. 在页面右上角的「API Key」输入框中粘贴你的 Key
2. 点击「✓ 验证」按钮
3. 看到绿色圆点亮起，表示验证成功

### 第四步：选择输出类型

根据你的需求，点击选择一种输出类型：

| 类型 | 适用场景 |
|------|---------|
| 🎨 图像生成 | 生成图片的 Prompt，如插画、海报、产品图 |
| 📊 信息图表 | 数据可视化、流程图、总结图 |
| 🏗️ 代码架构 | 系统架构图、微服务拓扑、技术栈图 |

### 第五步：输入描述

在左侧「原始 Prompt 输入」文本框中，用自然语言描述你想要的内容。

**写描述的技巧：**
- 说清楚主题和标题
- 列出具体的数据或内容要点
- 描述想要的风格（颜色、字体、氛围等）

### 第六步：转换

点击「✨ 转换为 JSON Prompt」按钮，等待几秒钟。

### 第七步：获取结果

转换完成后，右侧会显示结构化的 JSON Prompt。你可以：
- 点击「📋 复制」复制到剪贴板
- 点击「💾 下载」保存为 JSON 文件

### 第八步：使用 JSON Prompt

将生成的 JSON Prompt 粘贴到支持结构化输入的 AI 绘图工具中（如 Midjourney、DALL-E、Stable Diffusion 等），即可生成更精准的图像。

---

## 功能特点

- 支持 3 种输出类型：图像生成、信息图表、代码架构图
- 基于豆包大模型 API
- 零依赖 Python 后端（仅使用标准库）
- 支持 Nginx 反向代理部署

## 快速开始

### 本地运行

1. **启动后端服务**

```bash
./start.sh
```

或手动启动：

```bash
python3 server.py
```

2. **打开前端页面**

用浏览器打开 `index.html`，或通过 HTTP 服务器访问：

```bash
python3 -m http.server 8080
```

然后访问 http://localhost:8080

3. **配置并使用**

- 输入你的豆包 API Key，点击「验证」
- 选择输出类型（图像/信息图表/代码架构）
- 在左侧输入自然语言描述
- 点击「转换为 JSON Prompt」

### 停止服务

```bash
./stop.sh
```

## 使用示例

### 示例 1：信息图表

**输入：**

```
请生成一张排班系统性能优化的总结图。标题是 Schedule Calendar 性能优化。

内容要体现三期优化：
- 一期：Max RT 从 26s 降到 21s
- 二期：P99 从 6.2s 降到 3.1s
- 三期：NPS 提升 124.9%

风格：涂鸦风格，马克笔触感，米色背景，黄色蓝色高光
```

**输出：**

```json
{
  "task": "generate_infographic",
  "title": {
    "text": "Schedule Calendar 性能优化",
    "style": "banner_ribbon"
  },
  "theme": {
    "visual_style": "doodle_sketch",
    "texture": "marker_pen_strokes"
  },
  "color_palette": {
    "background": "#F5F5DC",
    "primary_accent": "#FFD700",
    "secondary_accent": "#87CEEB"
  },
  "content_blocks": [
    {
      "header": "一期优化",
      "metrics": [{"label": "Max RT", "before": "26s", "after": "21s", "change": "-19%"}]
    },
    {
      "header": "二期优化",
      "metrics": [{"label": "P99", "before": "6.2s", "after": "3.1s", "change": "-50%"}]
    },
    {
      "header": "三期优化",
      "metrics": [{"label": "NPS", "change": "+124.9%"}]
    }
  ]
}
```

### 示例 2：代码架构图

**输入：**

```
画一个微服务架构图，包含：
- 前端：React 应用
- API 网关：Nginx
- 后端服务：用户服务、订单服务、支付服务
- 数据库：MySQL、Redis
- 消息队列：Kafka
```

**输出：**

```json
{
  "task": "generate_architecture_diagram",
  "title": {"text": "微服务架构图"},
  "layers": [
    {
      "name": "前端层",
      "components": [{"name": "React App", "type": "ui", "technology": "React"}]
    },
    {
      "name": "网关层",
      "components": [{"name": "API Gateway", "type": "gateway", "technology": "Nginx"}]
    },
    {
      "name": "服务层",
      "components": [
        {"name": "用户服务", "type": "service"},
        {"name": "订单服务", "type": "service"},
        {"name": "支付服务", "type": "service"}
      ]
    },
    {
      "name": "数据层",
      "components": [
        {"name": "MySQL", "type": "database"},
        {"name": "Redis", "type": "cache"},
        {"name": "Kafka", "type": "queue"}
      ]
    }
  ],
  "connections": [
    {"from": "react_app", "to": "api_gateway", "type": "arrow"},
    {"from": "api_gateway", "to": "user_service", "type": "arrow"}
  ]
}
```

### 示例 3：图像生成

**输入：**

```
一只橘猫坐在窗台上，望着窗外的雨天，室内暖色灯光，治愈系风格
```

**输出：**

```json
{
  "task": "generate_image",
  "subject": {
    "main": "橘猫",
    "details": ["坐姿", "望向窗外"],
    "attributes": {"color": "橘色", "state": "安静沉思"}
  },
  "environment": {
    "setting": "室内窗台",
    "lighting": {"type": "人工光", "color_temperature": "暖色"},
    "atmosphere": "温馨治愈",
    "weather": "雨天"
  },
  "style": {
    "artistic_style": "治愈系插画",
    "mood": "温暖、宁静"
  }
}
```

## 项目结构

```
prompt_helping/
├── server.py           # Python 后端代理服务
├── index.html          # 前端页面
├── prompts/            # System Prompt 模板
│   ├── image.txt       # 图像生成 prompt
│   ├── infographic.txt # 信息图表 prompt
│   └── architecture.txt# 代码架构 prompt
├── start.sh            # 启动脚本
├── stop.sh             # 停止脚本
└── README.md
```

## 服务器部署

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/prompt_helping;
    index index.html;

    # API 代理
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

### 端口配置

默认端口为 8088，可通过环境变量修改：

```bash
PORT=9000 python3 server.py
```

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/prompts` | GET | 获取可用的 prompt 类型列表 |
| `/prompts/{type}` | GET | 获取指定类型的 system prompt |
| `/v1/chat/completions` | POST | 代理到豆包 API |

## 系统要求

- Python 3.7+（无额外依赖）

## 安全说明

- API Key 存储在浏览器 localStorage，不会上传到服务器
- 后端仅做请求转发，不记录敏感信息

## License

MIT
