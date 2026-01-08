"""
JSON Prompt Converter - Flask 后端服务
用于转发请求到豆包 API，解决浏览器 CORS 限制
"""

import os
import requests
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# 配置
PORT = int(os.environ.get('PORT', 8088))
DOUBAO_API_URL = 'https://ark.cn-beijing.volces.com/api/v3'
PROMPTS_DIR = Path(__file__).parent / 'prompts'
STATIC_DIR = Path(__file__).parent

app = Flask(__name__, static_folder=str(STATIC_DIR))
CORS(app)

# 存储加载的 prompts
PROMPTS = {}


def load_prompts():
    """启动时加载所有 prompt 文件"""
    global PROMPTS
    prompt_files = {
        'image': 'image.txt',
        'infographic': 'infographic.txt',
        'architecture': 'architecture.txt'
    }

    for prompt_type, filename in prompt_files.items():
        filepath = PROMPTS_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                PROMPTS[prompt_type] = f.read()
            print(f"  ✓ 已加载 {prompt_type} prompt ({len(PROMPTS[prompt_type])} 字符)")
        else:
            print(f"  ✗ 未找到 {filepath}")

    print(f"\n  共加载 {len(PROMPTS)} 个 prompt 模板\n")


# 静态文件路由
@app.route('/')
def index():
    return send_from_directory(STATIC_DIR, 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)


# 健康检查
@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'Server is running'})


# 获取可用的 prompt 类型列表
@app.route('/prompts')
def get_prompts():
    return jsonify({
        'types': list(PROMPTS.keys()),
        'count': len(PROMPTS)
    })


# 获取指定类型的 prompt
@app.route('/prompts/<prompt_type>')
def get_prompt(prompt_type):
    if prompt_type in PROMPTS:
        return jsonify({
            'type': prompt_type,
            'content': PROMPTS[prompt_type]
        })
    else:
        return jsonify({
            'error': 'Prompt not found',
            'available': list(PROMPTS.keys())
        }), 404


# API 代理
@app.route('/v1/<path:path>', methods=['POST', 'OPTIONS'])
def proxy(path):
    if request.method == 'OPTIONS':
        return '', 204

    target_url = f"{DOUBAO_API_URL}/{path}"

    headers = {
        'Content-Type': 'application/json'
    }

    # 转发 Authorization 头
    auth_header = request.headers.get('Authorization')
    if auth_header:
        headers['Authorization'] = auth_header

    print(f"[PROXY] POST /v1/{path} -> {target_url}")

    try:
        response = requests.post(
            target_url,
            json=request.json,
            headers=headers,
            timeout=300  # 5分钟超时
        )
        return response.json(), response.status_code
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Proxy request failed', 'message': str(e)}), 500


if __name__ == '__main__':
    print("\n📂 正在加载 Prompt 模板...")
    load_prompts()

    print(f"""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   🚀 JSON Prompt Converter Server (Flask)                  ║
║                                                            ║
║   Server:    http://localhost:{PORT}                        ║
║   Health:    http://localhost:{PORT}/health                 ║
║                                                            ║
║   Prompts:   http://localhost:{PORT}/prompts                ║
║   API:       http://localhost:{PORT}/v1/chat/completions    ║
║                                                            ║
║   Press Ctrl+C to stop                                     ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """)

    app.run(host='0.0.0.0', port=PORT, debug=False)
