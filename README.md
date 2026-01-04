# JSON Prompt Converter (Python 版)

将自然语言提示词智能转换为结构化 JSON Prompting 的工具。

## 🚀 快速开始

### 1. 启动后端服务

```bash
cd json-prompt-converter-py
python server.py
```

或者指定端口：

```bash
PORT=8080 python server.py
```

看到以下输出表示启动成功：

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   🚀 JSON Prompt Converter Proxy Server (Python)           ║
║                                                            ║
║   Server running at: http://localhost:3000                 ║
║   Health check:      http://localhost:3000/health          ║
║                                                            ║
║   API Proxy:         http://localhost:3000/v1/messages     ║
║                                                            ║
║   Press Ctrl+C to stop                                     ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

### 2. 打开前端页面

用浏览器打开 `index.html` 文件。

### 3. 配置 API Key

1. 在 "Claude API Key" 输入框中填入你的 API Key（格式：`sk-ant-xxx`）
2. 点击「测试」验证代理服务器连接
3. 点击「验证」测试 API Key 是否有效

### 4. 开始使用

1. 选择输出类型（图像/视频/信息图表等）
2. 在左侧文本框粘贴你的自然语言描述
3. 点击「✨ 转换为 JSON Prompt」
4. 复制或下载生成的 JSON

## 📁 项目结构

```
json-prompt-converter-py/
├── server.py          # Python 后端代理（零依赖）
├── index.html         # 前端页面
├── requirements.txt   # 依赖说明（当前为空）
└── README.md          # 说明文档
```

## ⚙️ 系统要求

- Python 3.7+（使用标准库，无需安装额外依赖）

## 🔧 配置说明

### 代理服务器端口

默认端口为 3000，可通过环境变量修改：

```bash
# Linux/Mac
PORT=8080 python server.py

# Windows (PowerShell)
$env:PORT=8080; python server.py

# Windows (CMD)
set PORT=8080 && python server.py
```

### 支持的输出类型

| 类型 | 说明 |
|------|------|
| 🎨 图像生成 | 生成图像的结构化 prompt |
| 🎬 视频生成 | 生成视频的结构化 prompt |
| 📊 信息图表 | 生成信息图表的结构化 prompt |
| 📝 内容创作 | 文章、博客等内容的结构化 prompt |
| 🔢 数据提取 | 数据提取任务的结构化 prompt |
| 💻 代码生成 | 代码生成的结构化 prompt |
| ⚙️ 自定义 | 自由格式 |

## 🔐 安全说明

- API Key 仅在本地存储（localStorage），不会上传到任何服务器
- 代理服务器仅做请求转发，不记录任何敏感信息
- 建议在本地开发环境使用，生产环境请添加适当的安全措施

## 📝 示例

### 输入（自然语言）

```
请生成一张排班系统性能优化的总结图。标题是 Schedule Calendar 性能优化。

内容要体现三期优化：
- 一期：Max RT 从 26s 降到 21s
- 二期：P99 从 6.2s 降到 3.1s  
- 三期：NPS 提升 124.9%

风格：涂鸦风格，马克笔触感，米色背景，黄色蓝色高光
```

### 输出（JSON Prompt）

```json
{
  "task": "generate_infographic",
  "title": {
    "text": "Schedule Calendar 性能优化",
    "style": "banner_ribbon"
  },
  "theme": {
    "core_message": "排班性能专项分三期优化",
    "visual_style": "doodle_sketch"
  },
  "color_palette": {
    "background": "#F5F5DC",
    "primary": "#FFD700",
    "accent": ["#87CEEB", "#000000"]
  },
  "content_blocks": [
    {
      "header": "一期优化",
      "data": [{"label": "Max RT", "before": "26s", "after": "21s"}]
    },
    {
      "header": "二期优化", 
      "data": [{"label": "P99", "before": "6.2s", "after": "3.1s"}]
    },
    {
      "header": "三期优化",
      "data": [{"label": "NPS", "value": "+124.9%"}]
    }
  ],
  "style": {
    "texture": "marker_pen_strokes",
    "outline": "black_hand_drawn_borders"
  }
}
```

## 🐛 常见问题

### Q: 提示 "Connection refused"
A: 确保后端服务已启动，检查端口是否正确

### Q: 提示 "Invalid API Key"
A: 检查 API Key 格式是否正确（sk-ant-xxx），确保有足够余额

### Q: 中文显示乱码
A: 确保浏览器编码设置为 UTF-8

## 📄 License

MIT
