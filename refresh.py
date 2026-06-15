#!/usr/bin/env python3
"""
京东校园招聘自动刷新活跃度脚本
"""
import os
import sys
import json
import time
import requests
from datetime import datetime


class JDCampusRefresh:
    """京东校园招聘活跃度刷新器"""

    def __init__(self):
        # 从环境变量读取 Cookie
        self.cookie = os.getenv('JD_COOKIE', '')

        # 投递记录 ID（写死，从 HAR 文件中提取）
        # 如需修改，直接编辑这里的列表
        self.delivery_record_ids = [3802615]

        # API 端点
        self.check_url = "https://campus.jd.com/api/wx/resume/checkCanResumeRefresh"
        self.refresh_url = "https://campus.jd.com/api/wx/resume/refresh"

        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://campus.jd.com/api/wx/position/index?type=internship',
            'Cookie': self.cookie
        }

    def validate_config(self):
        """验证配置是否完整"""
        if not self.cookie:
            print("❌ 错误: 未配置 JD_COOKIE 环境变量")
            return False

        if not self.delivery_record_ids:
            print("❌ 错误: 投递记录 ID 列表为空，请在代码中配置")
            return False

        return True

    def test_cookie_validity(self):
        """测试 Cookie 是否有效（首次运行时验证）"""
        print("🔍 验证 Cookie 有效性...")
        try:
            # 使用获取投递列表 API 来验证 Cookie
            url = "https://campus.jd.com/api/wx/delivery/officialInfo/list"
            payload = {"pageNo": 1, "pageSize": 1}

            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            if data.get('success'):
                print("✅ Cookie 有效！\n")
                return True
            else:
                error_msg = data.get('message', '未知错误')
                print(f"❌ Cookie 无效: {error_msg}\n")
                return False

        except requests.exceptions.RequestException as e:
            print(f"❌ Cookie 验证失败: {e}\n")
            return False
        except Exception as e:
            print(f"❌ 验证过程出错: {e}\n")
            return False

    def check_can_refresh(self, delivery_record_id):
        """检查是否可以刷新活跃度"""
        try:
            payload = {"deliveryRecordId": delivery_record_id}
            response = requests.post(
                self.check_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            print(f"  检查结果: {json.dumps(data, ensure_ascii=False)}")

            if data.get('success'):
                return True, data.get('body', {})
            else:
                return False, data

        except requests.exceptions.RequestException as e:
            print(f"  ❌ 检查请求失败: {e}")
            return False, {}
        except json.JSONDecodeError as e:
            print(f"  ❌ 解析响应失败: {e}")
            return False, {}

    def refresh_activity(self, delivery_record_id):
        """刷新活跃度"""
        try:
            payload = {"deliveryRecordId": delivery_record_id}
            response = requests.post(
                self.refresh_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            print(f"  刷新结果: {json.dumps(data, ensure_ascii=False)}")

            if data.get('success'):
                notice_msg = data.get('body', {}).get('noticeMsg', '刷新成功')
                print(f"  ✅ {notice_msg}")
                return True
            else:
                error_msg = data.get('message', '刷新失败')
                print(f"  ❌ {error_msg}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"  ❌ 刷新请求失败: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"  ❌ 解析响应失败: {e}")
            return False

    def run(self):
        """执行刷新任务"""
        print(f"\n{'='*60}")
        print(f"🚀 京东校园招聘活跃度刷新任务")
        print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        # 验证配置
        if not self.validate_config():
            sys.exit(1)

        # 首次验证 Cookie 是否有效
        if not self.test_cookie_validity():
            print("❌ Cookie 验证失败，请检查 JD_COOKIE 配置是否正确")
            print("💡 提示：请重新获取 Cookie 并更新 GitHub Secret")
            sys.exit(1)

        # 投递记录 ID 列表
        record_ids = self.delivery_record_ids

        if not record_ids:
            print("❌ 错误: 投递记录 ID 列表为空")
            sys.exit(1)

        print(f"📋 待刷新的投递记录数量: {len(record_ids)}\n")

        success_count = 0
        fail_count = 0

        # 处理每个投递记录
        for idx, record_id in enumerate(record_ids, 1):
            print(f"[{idx}/{len(record_ids)}] 处理投递记录: {record_id}")

            # 先检查是否可以刷新
            can_refresh, check_data = self.check_can_refresh(record_id)

            if can_refresh:
                # 执行刷新
                time.sleep(2)  # 避免请求过快
                if self.refresh_activity(record_id):
                    success_count += 1
                else:
                    fail_count += 1
            else:
                print(f"  ⚠️ 暂时无法刷新")
                fail_count += 1

            print()

            # 如果还有下一条记录，等待 3 秒
            if idx < len(record_ids):
                time.sleep(3)

        # 统计结果
        print(f"{'='*60}")
        print(f"📊 执行结果统计:")
        print(f"  ✅ 成功: {success_count}")
        print(f"  ❌ 失败: {fail_count}")
        print(f"  📝 总计: {len(record_ids)}")
        print(f"{'='*60}\n")

        # 如果全部失败，退出码为 1
        if fail_count == len(record_ids):
            sys.exit(1)


if __name__ == '__main__':
    refresher = JDCampusRefresh()
    refresher.run()
