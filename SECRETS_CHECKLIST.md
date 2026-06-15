# 🎯 GitHub Actions Secrets 配置清单

## 需要在 GitHub 配置的 Secrets

前往你的仓库：`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

---

### ✅ 必需配置（2 项）

| Secret 名称 | 说明 | 获取方式 |
|------------|------|---------|
| **JD_COOKIE** | 京东校园招聘完整 Cookie | 见下方详细说明 |
| **JD_DELIVERY_RECORD_IDS** | 投递记录 ID 列表（逗号分隔） | 见下方详细说明 |

---

## 📋 详细获取方法

### 1️⃣ JD_COOKIE - 如何获取

**步骤**：
1. Chrome 浏览器打开 https://campus.jd.com/
2. 登录你的账号
3. 按 **F12** 打开开发者工具
4. 切换到 **`Application`** 标签页（中文：应用）
5. 左侧展开 **`Cookies`** → **`https://campus.jd.com`**
6. 复制所有 Cookie

**格式**：
```
key1=value1; key2=value2; key3=value3; ...
```

**示例**：
```
3AB9D23F7A4B3CSS=ABC123DEF456; __jda=122270672.123456789.1234567890.1234567890.1234567890.12; __jdb=122270672.3.123456789|2.1234567890; __jdc=campus_jd_com; __jdu=1234567890; thor=ABCDEF123456
```

**必须包含的关键字段**：
- ✅ `3AB9D23F7A4B3CSS` - 会话认证（最重要）
- ✅ `__jda` - 京东分析
- ✅ `__jdb` - 京东设备标识
- ✅ `__jdc` - 京东客户端标识
- ✅ `__jdu` - 京东用户标识
- ✅ `thor` - 雷神系统标识

---

### 2️⃣ JD_DELIVERY_RECORD_IDS - 如何获取

#### 🔧 方法一：浏览器开发者工具抓包（推荐）

1. 在京东校园招聘页面按 **F12** 打开开发者工具
2. 切换到 **`Network`**（网络）标签页
3. 找到你已投递的职位，点击 **"刷新活跃度"** 按钮
4. 在网络请求列表中找到 `checkCanResumeRefresh` 或 `refresh` 请求
5. 点击该请求，查看 **`Payload`** 或 **`Request Body`**
6. 找到 `deliveryRecordId` 字段，这个数字就是投递记录 ID

**示例**：
```json
{
  "deliveryRecordId": 3802615
}
```

#### 🔧 方法二：调用 API 获取投递列表

**使用 curl**：
```bash
curl -X POST 'https://campus.jd.com/api/wx/delivery/officialInfo/list' \
  -H 'Cookie: 你的完整Cookie' \
  -H 'Content-Type: application/json' \
  --data-raw '{"pageNo":1,"pageSize":20}'
```

**使用 PowerShell**：
```powershell
$headers = @{
    "Cookie" = "你的完整Cookie"
    "Content-Type" = "application/json"
}
$body = @{
    pageNo = 1
    pageSize = 20
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://campus.jd.com/api/wx/delivery/officialInfo/list" `
    -Method POST -Headers $headers -Body $body
```

**返回数据结构**：
```json
{
  "success": true,
  "body": {
    "data": {
      "list": [
        {
          "deliveryRecordId": 3802615,
          "positionName": "前端开发工程师",
          ...
        },
        {
          "deliveryRecordId": 3802616,
          "positionName": "后端开发工程师",
          ...
        }
      ]
    }
  }
}
```

**配置格式**（多个 ID 用逗号分隔）：
```
3802615,3802616,3802617
```

---

## 🚀 配置完成后的检查清单

- [ ] 已添加 `JD_COOKIE` Secret
- [ ] 已添加 `JD_DELIVERY_RECORD_IDS` Secret
- [ ] 已在 Actions 标签页启用工作流
- [ ] 已手动触发一次测试（可选）
- [ ] 查看执行日志确认无误

---

## ⏰ 定时执行计划

脚本将在以下时间自动执行：
- 🌅 **北京时间 09:00**（UTC 01:00）
- 🌙 **北京时间 21:00**（UTC 13:00）

> 因为京东规定刷新后需等待 8 小时，所以每 12 小时执行一次。

---

## 🔍 如何验证配置是否正确

### 方法 1：手动触发测试
1. 进入仓库的 **`Actions`** 标签页
2. 选择 **`京东校园招聘活跃度刷新`** 工作流
3. 点击 **`Run workflow`** → **`Run workflow`**
4. 等待执行完成
5. 点击执行记录查看日志

### 方法 2：本地测试（推荐）
```bash
# 克隆仓库
git clone https://github.com/MARYCOMPLEX/jd-refresh.git
cd jd-refresh

# 安装依赖
pip install -r requirements.txt

# 运行测试脚本（会提示输入 Cookie 和 ID）
python test_local.py
```

---

## ⚠️ 注意事项

1. **Cookie 有效期**：
   - Cookie 可能会过期（通常几天到几周）
   - 如果脚本执行失败，需要重新获取 Cookie 并更新 Secret

2. **安全性**：
   - ❌ 不要将 Cookie 分享给任何人
   - ❌ 不要在公开场合展示你的 Cookie
   - ✅ 定期更新 Cookie
   - ✅ 如果怀疑 Cookie 泄露，立即修改密码

3. **刷新限制**：
   - 刷新后需要等待 **8 小时**才能再次刷新
   - 脚本会自动检查是否可以刷新
   - 如果在冷却期内，会跳过该记录

4. **请求频率**：
   - 脚本已内置请求间隔（2-3 秒）
   - 避免修改请求间隔过短，可能导致封号

---

## 📊 执行日志示例

成功执行的日志应该类似这样：

```
============================================================
🚀 京东校园招聘活跃度刷新任务
⏰ 执行时间: 2026-06-16 09:00:00
============================================================

📋 待刷新的投递记录数量: 2

[1/2] 处理投递记录: 3802615
  检查结果: {"success":true,"body":{"canRefresh":true}}
  刷新结果: {"success":true,"body":{"success":true,"noticeMsg":"简历已成功置顶！在8小时后可以再次刷新活跃度～"}}
  ✅ 简历已成功置顶！在8小时后可以再次刷新活跃度～

[2/2] 处理投递记录: 3802616
  检查结果: {"success":true,"body":{"canRefresh":true}}
  刷新结果: {"success":true,"body":{"success":true,"noticeMsg":"简历已成功置顶！在8小时后可以再次刷新活跃度～"}}
  ✅ 简历已成功置顶！在8小时后可以再次刷新活跃度～

============================================================
📊 执行结果统计:
  ✅ 成功: 2
  ❌ 失败: 0
  📝 总计: 2
============================================================
```

---

## 💡 常见问题

### Q1: 为什么执行失败？
**可能原因**：
- Cookie 已过期 → 重新获取并更新
- 投递记录 ID 错误 → 检查 ID 是否正确
- 还在冷却期内 → 等待 8 小时后再试
- 网络问题 → 查看 Actions 日志

### Q2: 如何修改执行时间？
编辑 `.github/workflows/refresh.yml` 文件中的 `cron` 表达式：
```yaml
schedule:
  - cron: '0 1,13 * * *'  # UTC 时间
```

**Cron 表达式说明**：
- `0 1 * * *` = UTC 01:00（北京时间 09:00）
- `0 13 * * *` = UTC 13:00（北京时间 21:00）

### Q3: Cookie 多久会过期？
通常 **几天到几周**，具体取决于京东的策略。建议每周检查一次。

---

## 📞 技术支持

如有问题，请在 GitHub 仓库提 Issue：
https://github.com/MARYCOMPLEX/jd-refresh/issues
