# 🎯 京东校园招聘自动刷新 - 完整配置清单

## ✅ 项目已完成

仓库地址：https://github.com/MARYCOMPLEX/jd-refresh

## 📦 项目文件结构

```
jd-refresh/
├── .github/
│   └── workflows/
│       └── refresh.yml          # GitHub Actions 工作流配置
├── refresh.py                   # 主刷新脚本
├── verify_cookie.py             # Cookie 验证工具（推荐先用这个）
├── test_local.py                # 本地测试脚本
├── requirements.txt             # Python 依赖
├── README.md                    # 完整使用文档
├── QUICK_START.md               # 5 分钟快速开始指南
├── SECRETS_CHECKLIST.md         # GitHub Secrets 详细配置清单
├── CONFIG_GUIDE.md              # 详细配置指南
├── LICENSE                      # MIT 许可证
└── .gitignore                   # Git 忽略文件
```

---

## 🔑 需要在 GitHub Actions 配置的 Secrets（必需）

在仓库 `Settings` → `Secrets and variables` → `Actions` 中添加：

### 1. JD_COOKIE

**说明**：京东校园招聘的完整 Cookie 字符串

**获取方式**：
1. Chrome 浏览器打开 https://campus.jd.com/
2. 登录账号
3. 按 F12 → Application → Cookies → https://campus.jd.com
4. 复制所有 Cookie

**格式示例**：
```
3AB9D23F7A4B3CSS=ABC123...; __jda=123.456...; __jdb=789...; __jdc=campus_jd_com; __jdu=345678901; thor=ABCD1234...
```

**必须包含的关键字段**：
- `3AB9D23F7A4B3CSS` - 会话认证（最重要）
- `__jda`, `__jdb`, `__jdc`, `__jdu` - 京东标识
- `thor` - 雷神系统标识

---

### 2. JD_DELIVERY_RECORD_IDS

**说明**：投递记录 ID 列表，多个 ID 用英文逗号分隔

**推荐获取方式**（使用验证工具）：
```bash
git clone https://github.com/MARYCOMPLEX/jd-refresh.git
cd jd-refresh
pip install -r requirements.txt
python verify_cookie.py
```

**手动获取方式**（开发者工具抓包）：
1. F12 打开开发者工具 → Network 标签页
2. 点击"刷新活跃度"按钮
3. 找到 `checkCanResumeRefresh` 请求
4. 查看 Payload 中的 `deliveryRecordId`

**格式示例**：
```
3802615,3802616,3802617
```

---

## ⏰ 自动执行时间

脚本将自动在以下时间执行：
- 🌅 **北京时间 09:00**（UTC 01:00）
- 🌙 **北京时间 21:00**（UTC 13:00）

每 12 小时执行一次（因为京东规定刷新后需等待 8 小时）

---

## 🚀 快速开始步骤

### 第 1 步：本地验证（推荐）

```bash
# 克隆仓库
git clone https://github.com/MARYCOMPLEX/jd-refresh.git
cd jd-refresh

# 安装依赖
pip install -r requirements.txt

# 验证 Cookie（会自动获取投递记录 ID）
python verify_cookie.py
```

### 第 2 步：Fork 仓库并配置 Secrets

1. 访问 https://github.com/MARYCOMPLEX/jd-refresh
2. 点击右上角 **Fork** 按钮
3. 进入你的仓库 → **Settings** → **Secrets and variables** → **Actions**
4. 添加 `JD_COOKIE` 和 `JD_DELIVERY_RECORD_IDS` 两个 Secrets

### 第 3 步：启用 Actions

1. 进入 **Actions** 标签页
2. 点击 **"I understand my workflows, go ahead and enable them"**

### 第 4 步：手动测试（可选）

1. 在 **Actions** 标签页选择 **"京东校园招聘活跃度刷新"**
2. 点击 **Run workflow** → **Run workflow**
3. 查看执行日志确认成功

---

## 📊 执行结果示例

成功执行的日志：

```
============================================================
🚀 京东校园招聘活跃度刷新任务
⏰ 执行时间: 2026-06-16 09:00:00
============================================================

📋 待刷新的投递记录数量: 2

[1/2] 处理投递记录: 3802615
  检查结果: {"success":true,"body":{"canRefresh":true}}
  刷新结果: {"success":true,"body":{"noticeMsg":"简历已成功置顶！在8小时后可以再次刷新活跃度～"}}
  ✅ 简历已成功置顶！在8小时后可以再次刷新活跃度～

[2/2] 处理投递记录: 3802616
  检查结果: {"success":true,"body":{"canRefresh":true}}
  刷新结果: {"success":true,"body":{"noticeMsg":"简历已成功置顶！在8小时后可以再次刷新活跃度～"}}
  ✅ 简历已成功置顶！在8小时后可以再次刷新活跃度～

============================================================
📊 执行结果统计:
  ✅ 成功: 2
  ❌ 失败: 0
  📝 总计: 2
============================================================
```

---

## 🛠️ 本地测试工具

### 工具 1：verify_cookie.py（推荐优先使用）

**功能**：
- ✅ 验证 Cookie 是否有效
- 📋 自动获取所有投递记录 ID
- 💡 直接生成配置值

**使用**：
```bash
python verify_cookie.py
```

### 工具 2：test_local.py

**功能**：
- 测试完整的刷新流程
- 验证 Cookie 和投递记录 ID 是否正确

**使用**：
```bash
python test_local.py
```

### 工具 3：refresh.py（主脚本）

**功能**：
- GitHub Actions 实际执行的脚本
- 也可以本地手动执行

**使用**：
```bash
# Windows (PowerShell)
$env:JD_COOKIE="你的Cookie"
$env:JD_DELIVERY_RECORD_IDS="3802615,3802616"
python refresh.py

# Linux / macOS
export JD_COOKIE="你的Cookie"
export JD_DELIVERY_RECORD_IDS="3802615,3802616"
python refresh.py
```

---

## 📚 文档说明

| 文档 | 用途 | 推荐阅读顺序 |
|------|------|-------------|
| **QUICK_START.md** | 5 分钟快速开始 | ⭐ 第 1 步 |
| **SECRETS_CHECKLIST.md** | Secrets 详细配置指南 | ⭐ 第 2 步 |
| **README.md** | 完整使用文档 | 📖 参考 |
| **CONFIG_GUIDE.md** | 详细配置说明 | 📖 参考 |
| **THIS_FILE.md** | 总体配置清单 | 📖 总览 |

---

## ⚠️ 重要注意事项

### Cookie 安全

- ❌ **不要**将 Cookie 分享给任何人
- ❌ **不要**在公开场合展示 Cookie
- ✅ **定期更新** Cookie（建议每周检查）
- ✅ **如果怀疑泄露**，立即修改密码

### Cookie 有效期

- Cookie 通常几天到几周会过期
- 如果脚本执行失败，检查是否 Cookie 过期
- 重新获取 Cookie 并更新 Secret

### 刷新限制

- 刷新后需要等待 **8 小时**才能再次刷新
- 脚本会自动检查，无需手动控制
- 如果在冷却期内，会跳过该记录

### 请求频率

- 脚本已内置 2-3 秒请求间隔
- **不要修改**请求间隔过短
- 避免频繁请求导致账号异常

---

## 🔍 常见问题

### Q1: 为什么执行失败？

**可能原因**：
1. Cookie 已过期 → 重新获取并更新 Secret
2. 投递记录 ID 错误 → 使用 `verify_cookie.py` 重新获取
3. 还在 8 小时冷却期内 → 正常现象，等待下次执行
4. 网络问题 → 查看 Actions 日志详情

### Q2: 如何修改执行时间？

编辑 `.github/workflows/refresh.yml` 中的 `cron` 表达式：

```yaml
schedule:
  - cron: '0 1,13 * * *'  # UTC 时间（北京时间 -8）
```

**常用时间**：
- `0 1 * * *` = UTC 01:00（北京时间 09:00）
- `0 13 * * *` = UTC 13:00（北京时间 21:00）
- `0 0 * * *` = UTC 00:00（北京时间 08:00）
- `0 12 * * *` = UTC 12:00（北京时间 20:00）

### Q3: 可以刷新多个投递记录吗？

可以！在 `JD_DELIVERY_RECORD_IDS` 中用逗号分隔多个 ID：
```
3802615,3802616,3802617,3802618
```

### Q4: Cookie 多久需要更新一次？

通常几天到几周，建议：
- 每周检查一次执行日志
- 如果失败，重新获取 Cookie
- 设置日历提醒每月更新一次

---

## 📞 获取帮助

- 🐛 报告 Bug：https://github.com/MARYCOMPLEX/jd-refresh/issues
- 💡 功能建议：提交 Issue 或 Pull Request
- 📖 完整文档：查看仓库中的各个 MD 文件

---

## ✅ 配置检查清单

使用前请确认：

- [ ] 已获取完整的 Cookie
- [ ] 已使用 `verify_cookie.py` 验证 Cookie 有效
- [ ] 已获取所有投递记录 ID
- [ ] 已 Fork 仓库到自己账号
- [ ] 已添加 `JD_COOKIE` Secret
- [ ] 已添加 `JD_DELIVERY_RECORD_IDS` Secret
- [ ] 已启用 GitHub Actions
- [ ] 已手动测试一次并查看日志
- [ ] 确认执行成功

---

## 🎉 完成！

现在你的京东校园招聘简历将自动保持活跃度，每天 2 次自动刷新！

祝你求职顺利！🚀
