#!/usr/bin/env python3
"""
设置页功能测试脚本
测试设置页的各项功能：配置保存、API 验证、状态指示器、LocalStorage 持久化
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8088"

def test_health_check():
    """测试健康检查端点"""
    print("\n📋 测试 1: 健康检查")
    try:
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'ok'
        print("   ✓ 健康检查通过")
        return True
    except Exception as e:
        print(f"   ✗ 健康检查失败：{e}")
        return False

def test_settings_page_load():
    """测试设置页加载"""
    print("\n📋 测试 2: 设置页加载")
    try:
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        html = response.text
        
        # 验证 UI 结构
        assert 'page-settings' in html, "缺少设置页容器"
        assert '⚙️ API 与模型配置' in html, "缺少统一的配置卡片标题"
        assert 'id="baseUrl"' in html, "缺少 Base URL 输入框"
        assert 'id="modelName"' in html, "缺少模型名称输入框"
        assert 'id="apiKey"' in html, "缺少 API Key 输入框"
        assert 'id="apiStatus"' in html, "缺少状态指示器"
        assert 'saveAndTestConfig()' in html, "缺少保存验证函数"
        assert 'form-hint' in html, "缺少表单提示样式"
        assert 'form-actions' in html, "缺少表单操作区样式"
        
        print("   ✓ 设置页 HTML 结构正确")
        print("   ✓ 统一的 API 与模型配置卡片")
        print("   ✓ Base URL、模型名称、API Key 输入框存在")
        print("   ✓ 状态指示器存在")
        print("   ✓ 表单提示和操作区样式存在")
        return True
    except Exception as e:
        print(f"   ✗ 设置页加载失败：{e}")
        return False

def test_prompts_endpoint():
    """测试 Prompt 模板端点"""
    print("\n📋 测试 3: Prompt 模板端点")
    try:
        response = requests.get(f"{BASE_URL}/prompts")
        assert response.status_code == 200
        data = response.json()
        assert 'types' in data
        assert 'count' in data
        print(f"   ✓ 可用 Prompt 类型：{len(data['types'])} 个")
        
        # 测试获取具体模板
        for prompt_type in ['image', 'optimizer_rtf']:
            response = requests.get(f"{BASE_URL}/prompts/{prompt_type}")
            assert response.status_code == 200
            data = response.json()
            assert 'content' in data
        print("   ✓ Prompt 模板获取正常")
        return True
    except Exception as e:
        print(f"   ✗ Prompt 模板端点失败：{e}")
        return False

def test_api_proxy_without_key():
    """测试 API 代理（无 API Key 时应失败）"""
    print("\n📋 测试 4: API 代理（无 API Key）")
    try:
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json={
                "model": "test-model",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hi"}]
            },
            headers={
                "Content-Type": "application/json",
                "X-Base-URL": "https://ark.cn-beijing.volces.com/api/v3"
            }
        )
        # 没有 API Key 应该返回 401 或 403
        assert response.status_code in [401, 403, 400], f"预期 401/403/400，实际 {response.status_code}"
        print(f"   ✓ 无 API Key 时正确拒绝请求 (状态码：{response.status_code})")
        return True
    except Exception as e:
        print(f"   ✗ API 代理测试失败：{e}")
        return False

def test_api_proxy_with_invalid_key():
    """测试 API 代理（无效 API Key 时应失败）"""
    print("\n📋 测试 5: API 代理（无效 API Key）")
    try:
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json={
                "model": "test-model",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hi"}]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer invalid-key",
                "X-Base-URL": "https://ark.cn-beijing.volces.com/api/v3"
            }
        )
        # 无效 API Key 应该返回 401
        assert response.status_code in [401, 400], f"预期 401/400，实际 {response.status_code}"
        print(f"   ✓ 无效 API Key 时正确拒绝请求 (状态码：{response.status_code})")
        return True
    except Exception as e:
        print(f"   ✗ API 代理测试失败：{e}")
        return False

def test_javascript_logic():
    """测试前端 JavaScript 逻辑"""
    print("\n📋 测试 6: 前端 JavaScript 逻辑")
    try:
        response = requests.get(f"{BASE_URL}/")
        html = response.text
        
        # 验证关键函数存在
        assert 'function getConfig()' in html, "缺少 getConfig 函数"
        assert 'function saveConfig(' in html, "缺少 saveConfig 函数"
        assert 'function setConfigured(' in html, "缺少 setConfigured 函数"
        assert 'function updateConfigStatus()' in html, "缺少 updateConfigStatus 函数"
        assert 'async function saveAndTestConfig()' in html, "缺少 saveAndTestConfig 函数"
        assert 'function toggleApiKeyVisibility()' in html, "缺少 toggleApiKeyVisibility 函数"
        
        print("   ✓ 配置管理函数存在 (getConfig, saveConfig, setConfigured)")
        print("   ✓ 状态更新函数存在 (updateConfigStatus)")
        print("   ✓ 保存验证函数存在 (saveAndTestConfig)")
        print("   ✓ API Key 可见性切换函数存在 (toggleApiKeyVisibility)")
        
        # 验证 LocalStorage 键名
        assert "'base_url'" in html, "缺少 base_url LocalStorage 键"
        assert "'model'" in html, "缺少 model LocalStorage 键"
        assert "'api_key'" in html, "缺少 api_key LocalStorage 键"
        assert "'api_configured'" in html, "缺少 api_configured LocalStorage 键"
        print("   ✓ LocalStorage 键名正确 (base_url, model, api_key, api_configured)")
        
        # 验证状态指示器的三种状态
        assert 'status-badge pending' in html, "缺少未配置/验证中状态样式"
        assert 'status-badge error' in html, "缺少验证失败状态样式"
        assert 'status-badge">' in html or 'status-badge ' in html, "缺少已验证状态样式"
        assert '未配置' in html, "缺少未配置状态文本"
        assert '验证中' in html, "缺少验证中状态文本"
        assert '已验证' in html, "缺少已验证状态文本"
        assert '验证失败' in html, "缺少验证失败状态文本"
        print("   ✓ 状态指示器三种状态完整 (未配置、验证中、已验证/验证失败)")
        
        # 验证页面加载时恢复配置
        assert "window.addEventListener('load'" in html, "缺少页面加载事件"
        assert "document.getElementById('baseUrl').value = config.baseUrl" in html, "缺少 Base URL 恢复"
        assert "document.getElementById('modelName').value = config.model" in html, "缺少模型名称恢复"
        assert "document.getElementById('apiKey').value = config.apiKey" in html, "缺少 API Key 恢复"
        print("   ✓ 页面加载时配置恢复逻辑存在")
        
        return True
    except Exception as e:
        print(f"   ✗ JavaScript 逻辑测试失败：{e}")
        return False

def test_css_styles():
    """测试 CSS 样式"""
    print("\n📋 测试 7: CSS 样式")
    try:
        response = requests.get(f"{BASE_URL}/")
        html = response.text
        
        # 验证关键样式存在
        assert '.form-hint' in html, "缺少 .form-hint 样式"
        assert '.form-actions' in html, "缺少 .form-actions 样式"
        assert '.status-badge' in html, "缺少 .status-badge 样式"
        assert '.status-badge.error' in html, "缺少 .status-badge.error 样式"
        assert '.status-badge.pending' in html, "缺少 .status-badge.pending 样式"
        
        print("   ✓ 表单提示样式 (.form-hint) 存在")
        print("   ✓ 表单操作区样式 (.form-actions) 存在")
        print("   ✓ 状态指示器样式 (.status-badge) 存在")
        print("   ✓ 状态指示器变体样式存在 (.error, .pending)")
        
        return True
    except Exception as e:
        print(f"   ✗ CSS 样式测试失败：{e}")
        return False

def test_save_and_test_config_logic():
    """测试 saveAndTestConfig 函数逻辑"""
    print("\n📋 测试 8: saveAndTestConfig 函数逻辑")
    try:
        response = requests.get(f"{BASE_URL}/")
        html = response.text
        
        # 验证函数逻辑
        assert "document.getElementById('baseUrl').value.trim()" in html, "缺少 Base URL 获取"
        assert "document.getElementById('modelName').value.trim()" in html, "缺少模型名称获取"
        assert "document.getElementById('apiKey').value.trim()" in html, "缺少 API Key 获取"
        
        # 验证输入验证
        assert "请输入 Base URL" in html, "缺少 Base URL 验证提示"
        assert "请输入模型名称" in html, "缺少模型名称验证提示"
        assert "请输入 API Key" in html, "缺少 API Key 验证提示"
        
        # 验证保存配置
        assert "saveConfig(baseUrl, modelName, apiKey)" in html, "缺少配置保存调用"
        
        # 验证状态切换
        assert "statusBadge.className = 'status-badge pending'" in html, "缺少验证中状态切换"
        assert "statusBadge.innerHTML = '<span>●</span> 验证中...'" in html, "缺少验证中状态文本"
        
        # 验证 API 请求
        assert "fetch('/v1/chat/completions'" in html, "缺少 API 验证请求"
        assert "'Authorization': `Bearer ${apiKey}`" in html, "缺少 Authorization 头"
        assert "'X-Base-URL': baseUrl" in html, "缺少 X-Base-URL 头"
        
        # 验证成功处理
        assert "setConfigured('true')" in html, "缺少成功状态设置"
        assert "配置保存成功" in html, "缺少成功提示"
        
        # 验证失败处理
        assert "setConfigured('false')" in html, "缺少失败状态设置"
        assert "statusBadge.className = 'status-badge error'" in html, "缺少失败状态切换"
        assert "验证失败" in html, "缺少失败提示"
        
        print("   ✓ 输入验证逻辑完整")
        print("   ✓ 配置保存逻辑正确")
        print("   ✓ 状态指示器切换逻辑正确")
        print("   ✓ API 验证请求正确（包含 Authorization 和 X-Base-URL 头）")
        print("   ✓ 成功/失败处理逻辑完整")
        
        return True
    except Exception as e:
        print(f"   ✗ saveAndTestConfig 函数逻辑测试失败：{e}")
        return False

def main():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 Prompt Studio 设置页功能测试")
    print("=" * 60)
    
    tests = [
        test_health_check,
        test_settings_page_load,
        test_prompts_endpoint,
        test_api_proxy_without_key,
        test_api_proxy_with_invalid_key,
        test_javascript_logic,
        test_css_styles,
        test_save_and_test_config_logic,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"   ✗ 测试异常：{e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果：{sum(results)}/{len(results)} 通过")
    print("=" * 60)
    
    if all(results):
        print("\n✅ 所有测试通过！")
        return 0
    else:
        print("\n❌ 部分测试失败，请检查上方输出")
        return 1

if __name__ == '__main__':
    sys.exit(main())
