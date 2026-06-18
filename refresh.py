#!/usr/bin/env python3
"""
京东校园招聘自动刷新活跃度脚本。

安全原则：
1. 启动后不做任何 Cookie/API 预检请求。
2. 只在北京时间 09:30 或 17:30 的目标窗口内发送刷新请求。
3. 请求发送前先记录状态，避免同一时段重复触发导致重复请求。
"""
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests


BEIJING_TZ = ZoneInfo("Asia/Shanghai")
TARGET_TIMES = ((9, 30), (17, 30))
EARLY_START_WINDOW = timedelta(minutes=30)
LATE_GRACE_WINDOW = timedelta(minutes=45)
COOLDOWN_PROTECTION = timedelta(hours=8, seconds=30)
STATE_PATH = Path(".refresh-state") / "state.json"


class JDCampusRefresh:
    """京东校园招聘活跃度刷新器"""

    def __init__(self):
        self.cookie = os.getenv("JD_COOKIE", "")
        self.delivery_record_ids = [3802615]
        self.refresh_url = "https://campus.jd.com/api/wx/resume/refresh"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/149.0.0.0 Safari/537.36"
            ),
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://campus.jd.com/api/wx/position/index?type=internship",
            "Origin": "https://campus.jd.com",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Cookie": self.cookie,
        }

    def now(self):
        return datetime.now(BEIJING_TZ)

    def validate_config(self):
        """只验证本地配置，不发送网络请求。"""
        if not self.cookie:
            print("错误: 未配置 JD_COOKIE 环境变量")
            return False

        if not self.delivery_record_ids:
            print("错误: 投递记录 ID 列表为空，请在代码中配置")
            return False

        return True

    def load_state(self):
        if not STATE_PATH.exists():
            return {"slots": {}}

        try:
            with STATE_PATH.open("r", encoding="utf-8") as f:
                state = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"状态文件读取失败，将按首次运行处理: {exc}")
            return {"slots": {}}

        if not isinstance(state, dict):
            return {"slots": {}}
        if not isinstance(state.get("slots"), dict):
            state["slots"] = {}
        return state

    def save_state(self, state):
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = STATE_PATH.with_suffix(".tmp")
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        tmp_path.replace(STATE_PATH)

    def parse_datetime(self, value):
        if not value:
            return None
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            return None

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=BEIJING_TZ)
        return parsed.astimezone(BEIJING_TZ)

    def target_datetimes_for_day(self, day):
        return [
            datetime(day.year, day.month, day.day, hour, minute, tzinfo=BEIJING_TZ)
            for hour, minute in TARGET_TIMES
        ]

    def current_target(self, now):
        for target in self.target_datetimes_for_day(now):
            if target - EARLY_START_WINDOW <= now <= target + LATE_GRACE_WINDOW:
                return target
        return None

    def next_target(self, now):
        candidates = self.target_datetimes_for_day(now)
        tomorrow = now + timedelta(days=1)
        candidates.extend(self.target_datetimes_for_day(tomorrow))
        return min(target for target in candidates if target > now)

    def slot_key(self, target):
        return target.strftime("%Y-%m-%d %H:%M")

    def wait_until(self, target, reason):
        while True:
            now = self.now()
            seconds = (target - now).total_seconds()
            if seconds <= 0:
                return

            if seconds > 60:
                print(f"等待{reason}: 还剩 {int(seconds // 60)} 分钟")
            else:
                print(f"等待{reason}: 还剩 {int(seconds)} 秒")

            time.sleep(max(1, min(60, seconds)))

    def latest_recorded_request_time(self, state):
        times = [
            self.parse_datetime(state.get("last_request_at")),
            self.parse_datetime(state.get("last_success_at")),
        ]
        times = [value for value in times if value]
        return max(times) if times else None

    def enforce_cooldown(self, state, target):
        """避免 09:30 实际发送延迟后，17:30 提前撞 8 小时冷却。"""
        last_request_at = self.latest_recorded_request_time(state)
        if not last_request_at:
            return True

        next_allowed_at = last_request_at + COOLDOWN_PROTECTION
        now = self.now()
        if now >= next_allowed_at:
            return True

        if next_allowed_at <= target + LATE_GRACE_WINDOW:
            print(
                "检测到上次刷新请求时间为 "
                f"{last_request_at.strftime('%Y-%m-%d %H:%M:%S')}，"
                f"为保护 8 小时冷却，将等到 {next_allowed_at.strftime('%H:%M:%S')} 再请求。"
            )
            self.wait_until(next_allowed_at, "8 小时冷却保护")
            return True

        print(
            "当前距离上次刷新请求不足 8 小时，且安全请求时间已超出本次窗口；"
            "本次不发送任何请求。"
        )
        return False

    def refresh_activity(self, delivery_record_id):
        """直接刷新活跃度。此方法是唯一会请求京东接口的地方。"""
        try:
            payload = {"deliveryRecordId": delivery_record_id}
            response = requests.post(
                self.refresh_url,
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            print(f"  刷新结果: {json.dumps(data, ensure_ascii=False)}")

            body = data.get("body", {})
            if isinstance(body, dict) and body.get("code") == 401:
                print("  认证失败: Cookie 可能已过期或无效")
                return False

            if data.get("success") and isinstance(body, dict) and body.get("success"):
                notice_msg = body.get("noticeMsg", "刷新成功")
                print(f"  成功: {notice_msg}")
                return True

            if isinstance(body, dict):
                error_msg = body.get("message") or body.get("noticeMsg") or "刷新失败"
            else:
                error_msg = data.get("message", "刷新失败")
            print(f"  失败: {error_msg}")
            return False

        except requests.exceptions.RequestException as exc:
            print(f"  刷新请求失败: {exc}")
            return False
        except json.JSONDecodeError as exc:
            print(f"  解析响应失败: {exc}")
            return False

    def run(self):
        now = self.now()
        print(f"\n{'=' * 60}")
        print("京东校园招聘活跃度刷新任务")
        print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')} (北京时间 UTC+8)")
        print("目标时间: 09:30 / 17:30 (北京时间 UTC+8)")
        print(f"{'=' * 60}\n")

        state = self.load_state()
        target = self.current_target(now)
        if not target:
            next_target = self.next_target(now)
            print(
                "当前不在目标刷新窗口内，不发送任何京东请求。"
                f"下一次目标时间: {next_target.strftime('%Y-%m-%d %H:%M:%S')} (北京时间)"
            )
            return

        slot_key = self.slot_key(target)
        slot_state = state.setdefault("slots", {}).get(slot_key, {})
        if slot_state.get("request_sent_at"):
            print(f"{slot_key} 这个时段已经发送过刷新请求，本次直接退出。")
            return

        if not self.validate_config():
            sys.exit(1)

        if now < target:
            print(
                f"Action 已提前启动；目标刷新时间是 "
                f"{target.strftime('%Y-%m-%d %H:%M:%S')}，到点前不会发送请求。"
            )
            self.wait_until(target, "目标刷新时间")

        state = self.load_state()
        slot_state = state.setdefault("slots", {}).get(slot_key, {})
        if slot_state.get("request_sent_at"):
            print(f"{slot_key} 这个时段已经发送过刷新请求，本次直接退出。")
            return

        if not self.enforce_cooldown(state, target):
            state["slots"][slot_key] = {
                **slot_state,
                "target_at": target.isoformat(),
                "skipped_at": self.now().isoformat(),
                "status": "skipped_cooldown",
            }
            self.save_state(state)
            return

        request_time = self.now()
        state["slots"][slot_key] = {
            **slot_state,
            "target_at": target.isoformat(),
            "request_sent_at": request_time.isoformat(),
            "status": "request_sent",
        }
        state["last_request_at"] = request_time.isoformat()
        self.save_state(state)
        print(f"已进入目标时段 {slot_key}，现在只发送真正的刷新请求。")
        print(f"待刷新的投递记录数量: {len(self.delivery_record_ids)}\n")

        success_count = 0
        fail_count = 0
        for idx, record_id in enumerate(self.delivery_record_ids, 1):
            print(f"[{idx}/{len(self.delivery_record_ids)}] 处理投递记录: {record_id}")
            if self.refresh_activity(record_id):
                success_count += 1
            else:
                fail_count += 1

            if idx < len(self.delivery_record_ids):
                time.sleep(3)
            print()

        completed_at = self.now()
        state = self.load_state()
        slot_state = state.setdefault("slots", {}).get(slot_key, {})
        state["slots"][slot_key] = {
            **slot_state,
            "completed_at": completed_at.isoformat(),
            "success_count": success_count,
            "fail_count": fail_count,
            "status": "success" if success_count > 0 and fail_count == 0 else "failed",
        }
        if success_count > 0:
            state["last_success_at"] = completed_at.isoformat()
        self.save_state(state)

        print(f"{'=' * 60}")
        print("执行结果统计:")
        print(f"  成功刷新: {success_count}")
        print(f"  失败: {fail_count}")
        print(f"  总计: {len(self.delivery_record_ids)}")
        print(f"{'=' * 60}\n")

        if fail_count > 0:
            print("本次已经发送过刷新请求。为避免重复消耗刷新机会，不自动重试。")
            print("请查看上方京东接口返回内容判断是否需要人工处理 Cookie 或投递记录 ID。")


if __name__ == "__main__":
    JDCampusRefresh().run()
