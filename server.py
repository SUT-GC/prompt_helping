"""
JSON Prompt Converter - Python 后端代理服务
用于转发请求到豆包 API，解决浏览器 CORS 限制
支持从文件加载 System Prompt
"""

import json
import http.server
import urllib.request
import urllib.error
from urllib.parse import urlparse
import ssl
import os
from datetime import datetime
from pathlib import Path

# 配置
PORT = int(os.environ.get('PORT', 8088))
DOUBAO_API_URL = 'https://ark.cn-beijing.volces.com/api/v3'
PROMPTS_DIR = Path(__file__).parent / 'prompts'

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


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    """代理请求处理器"""

    # CORS 头
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Max-Age': '86400',
    }

    def log_message(self, format, *args):
        """自定义日志格式"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if args:
            print(f"[{timestamp}] {args[0]}")
        else:
            print(f"[{timestamp}] {format}")

    def send_cors_headers(self):
        """发送 CORS 头"""
        for key, value in self.cors_headers.items():
            self.send_header(key, value)

    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)

        # 健康检查端点
        if parsed_path.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            response = {'status': 'ok', 'message': 'Proxy server is running'}
            self.wfile.write(json.dumps(response).encode())
            return

        # 获取可用的 prompt 类型列表
        if parsed_path.path == '/prompts':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            response = {
                'types': list(PROMPTS.keys()),
                'count': len(PROMPTS)
            }
            self.wfile.write(json.dumps(response).encode())
            return

        # 获取指定类型的 prompt
        if parsed_path.path.startswith('/prompts/'):
            prompt_type = parsed_path.path.replace('/prompts/', '')
            if prompt_type in PROMPTS:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                response = {
                    'type': prompt_type,
                    'content': PROMPTS[prompt_type]
                }
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode())
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Prompt not found',
                    'available': list(PROMPTS.keys())
                }).encode())
            return

        # 404
        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Not Found'}).encode())

    def do_POST(self):
        """处理 POST 请求 - 代理到豆包 API"""
        parsed_path = urlparse(self.path)

        # 只代理 /v1/ 路径
        if not parsed_path.path.startswith('/v1/'):
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not Found'}).encode())
            return

        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''

        # 构建目标 URL (豆包使用 /api/v3 路径)
        api_path = parsed_path.path.replace('/v1/', '/')
        target_url = f"{DOUBAO_API_URL}{api_path}"

        # 准备请求头
        proxy_headers = {
            'Content-Type': 'application/json',
        }

        # 转发 Authorization 头 (Bearer token)
        auth_header = self.headers.get('Authorization')
        if auth_header:
            proxy_headers['Authorization'] = auth_header

        self.log_message(f"POST {parsed_path.path} -> {target_url}")

        try:
            # 创建请求
            request = urllib.request.Request(
                target_url,
                data=body,
                headers=proxy_headers,
                method='POST'
            )

            # 创建 SSL 上下文
            ssl_context = ssl.create_default_context()

            # 发送请求
            with urllib.request.urlopen(request, context=ssl_context) as response:
                # 读取响应
                response_body = response.read()

                # 发送响应
                self.send_response(response.status)
                self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(response_body)

        except urllib.error.HTTPError as e:
            # HTTP 错误
            error_body = e.read().decode('utf-8')
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(error_body.encode())

        except urllib.error.URLError as e:
            # 网络错误
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            error_response = {'error': 'Proxy request failed', 'message': str(e.reason)}
            self.wfile.write(json.dumps(error_response).encode())

        except Exception as e:
            # 其他错误
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            error_response = {'error': 'Internal server error', 'message': str(e)}
            self.wfile.write(json.dumps(error_response).encode())


def run_server():
    """启动服务器"""
    print("\n📂 正在加载 Prompt 模板...")
    load_prompts()

    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, ProxyHandler)

    print(f"""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   🚀 JSON Prompt Converter Proxy Server                    ║
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

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped.")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()
