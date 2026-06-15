#!/usr/bin/env python3
"""
本地测试脚本 - 用于在本地调试刷新功能
"""
import os
import sys


def main():
    print("="*60)
    print("京东校园招聘活跃度刷新 - 本地测试")
    print("="*60)
    print()

    # 提示用户输入配置
    print("请按照提示输入配置信息（或按 Ctrl+C 取消）\n")

    # 获取 Cookie
    cookie = input("请输入完整的 Cookie: ").strip()
    if not cookie:
        print("❌ Cookie 不能为空")
        sys.exit(1)

    # 获取投递记录 ID
    delivery_ids = input("请输入投递记录 ID（多个用逗号分隔）: ").strip()
    if not delivery_ids:
        print("❌ 投递记录 ID 不能为空")
        sys.exit(1)

    # 设置环境变量
    os.environ['JD_COOKIE'] = cookie
    os.environ['JD_DELIVERY_RECORD_IDS'] = delivery_ids

    print("\n" + "="*60)
    print("开始执行刷新任务...")
    print("="*60 + "\n")

    # 导入并执行主脚本
    from refresh import JDCampusRefresh
    refresher = JDCampusRefresh()
    refresher.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户取消操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 执行出错: {e}")
        sys.exit(1)
