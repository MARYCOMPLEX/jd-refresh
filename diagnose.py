#!/usr/bin/env python3
"""
诊断脚本 - 对比两个 API 的请求差异
"""
import os
import sys
import requests
import json


def test_apis(cookie):
    """测试两个 API 的差异"""

    # 基础请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://campus.jd.com/api/wx/position/index?type=internship',
        'Origin': 'https://campus.jd.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Cookie': cookie
    }

    print("="*60)
    print("测试 1: 获取投递列表 API")
    print("="*60)

    try:
        response = requests.post(
            "https://campus.jd.com/api/wx/delivery/officialInfo/list",
            headers=headers,
            json={"pageNo": 1, "pageSize": 1},
            timeout=30
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"错误: {e}")

    print("\n")
    print("="*60)
    print("测试 2: 检查刷新 API")
    print("="*60)

    try:
        response = requests.post(
            "https://campus.jd.com/api/wx/resume/checkCanResumeRefresh",
            headers=headers,
            json={"deliveryRecordId": 3802615},
            timeout=30
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print(f"\n响应头:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"错误: {e}")

    print("\n")
    print("="*60)
    print("测试 3: 刷新活跃度 API")
    print("="*60)

    try:
        response = requests.post(
            "https://campus.jd.com/api/wx/resume/refresh",
            headers=headers,
            json={"deliveryRecordId": 3802615},
            timeout=30
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        print(f"\n响应头:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"错误: {e}")

    print("\n")
    print("="*60)
    print("💡 请在浏览器中手动刷新活跃度，然后：")
    print("   1. 打开开发者工具 (F12)")
    print("   2. Network 标签页")
    print("   3. 找到 'refresh' 请求")
    print("   4. 右键 → Copy → Copy as cURL (bash)")
    print("   5. 将 cURL 命令发送给我分析")
    print("="*60)


if __name__ == '__main__':
    print("\n京东校园招聘 API 诊断工具\n")

    cookie = input("请输入完整的 Cookie: ").strip()

    if not cookie:
        print("❌ Cookie 不能为空")
        sys.exit(1)

    print()
    test_apis(cookie)
