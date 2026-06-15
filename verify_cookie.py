#!/usr/bin/env python3
"""
快速验证 Cookie 是否有效
"""
import requests
import sys


def test_cookie(cookie):
    """测试 Cookie 是否有效"""
    print("正在验证 Cookie 有效性...")
    print("-" * 60)

    # 测试 API：获取投递列表
    url = "https://campus.jd.com/api/wx/delivery/officialInfo/list"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Cookie': cookie
    }
    payload = {
        "pageNo": 1,
        "pageSize": 20
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        if data.get('success'):
            print("✅ Cookie 有效！")
            print()

            # 显示投递记录
            delivery_list = data.get('body', {}).get('data', {}).get('list', [])

            if delivery_list:
                print(f"📋 找到 {len(delivery_list)} 条投递记录:")
                print()

                record_ids = []
                for idx, record in enumerate(delivery_list, 1):
                    record_id = record.get('deliveryRecordId', 'N/A')
                    position_name = record.get('positionName', '未知职位')
                    company_name = record.get('companyName', '未知公司')
                    status = record.get('statusStr', '未知状态')

                    print(f"[{idx}] ID: {record_id}")
                    print(f"    职位: {position_name}")
                    print(f"    公司: {company_name}")
                    print(f"    状态: {status}")
                    print()

                    if record_id != 'N/A':
                        record_ids.append(str(record_id))

                # 生成配置建议
                print("-" * 60)
                print("💡 建议的 GitHub Secrets 配置:")
                print()
                print("JD_DELIVERY_RECORD_IDS 的值:")
                print(",".join(record_ids))
                print()

            else:
                print("⚠️ 未找到投递记录，请先在京东校园招聘投递职位")

            return True

        else:
            error_msg = data.get('message', '未知错误')
            print(f"❌ Cookie 无效或已过期")
            print(f"错误信息: {error_msg}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return False


def main():
    print("="*60)
    print("京东校园招聘 Cookie 验证工具")
    print("="*60)
    print()

    cookie = input("请输入完整的 Cookie: ").strip()

    if not cookie:
        print("❌ Cookie 不能为空")
        sys.exit(1)

    print()

    if test_cookie(cookie):
        print("="*60)
        print("✅ 验证通过！可以在 GitHub Actions 中使用此 Cookie")
        print("="*60)
        sys.exit(0)
    else:
        print("="*60)
        print("❌ 验证失败！请重新获取 Cookie")
        print("="*60)
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户取消操作")
        sys.exit(0)
