# 京东校园招聘自动刷新活跃度

自动刷新京东校园招聘平台的简历活跃度，保持投递记录的曝光度。

## 功能特性

- ✅ 自动检查是否可以刷新活跃度
- ✅ 自动执行简历刷新操作
- ✅ 支持多个投递记录批量刷新
- ✅ GitHub Actions 定时自动执行
- ✅ 详细的执行日志和结果统计

## 使用方法

### 1. 获取必要的配置信息

在使用前，你需要获取以下信息：

#### 1.1 获取 Cookie

1. 使用 Chrome 浏览器打开 [京东校园招聘](https://campus.jd.com/)
2. 登录你的账号
3. 按 `F12` 打开开发者工具
4. 切换到 `Application` 标签页（或 `应用` 标签页）
5. 左侧展开 `Cookies` → `https://campus.jd.com`
6. 复制所有 Cookie（格式：`key1=value1; key2=value2; ...`）

**重要的 Cookie 字段**（至少需要这些）：
- `3AB9D23F7A4B3CSS` - 会话凭证
- `__jda` - 京东分析
- `__jdb` - 京东标识
- `__jdc` - 京东客户端
- `__jdu` - 京东用户
- `thor` - 雷神标识
- 其他可能的认证相关字段

#### 1.2 获取投递记录 ID (deliveryRecordId)

方法一：通过浏览器开发者工具抓包

1. 在京东校园招聘页面，打开开发者工具（F12）
2. 切换到 `Network` (网络) 标签页
3. 找到你已投递的职位，点击"刷新活跃度"按钮
4. 在网络请求中找到 `checkCanResumeRefresh` 或 `refresh` 请求
5. 查看请求的 `Payload` 或 `Request Body`，其中的 `deliveryRecordId` 就是投递记录 ID

方法二：通过 API 获取投递列表

```bash
curl -X POST 'https://campus.jd.com/api/wx/delivery/officialInfo/list' \
  -H 'Cookie: 你的完整Cookie' \
  -H 'Content-Type: application/json' \
  --data-raw '{"pageNo":1,"pageSize":20}'
```

返回的 JSON 中会包含所有投递记录的 `deliveryRecordId`。

### 2. 本地测试

克隆仓库：

```bash
git clone https://github.com/MARYCOMPLEX/jd-refresh.git
cd jd-refresh
```

安装依赖：

```bash
pip install -r requirements.txt
```

设置环境变量并测试：

```bash
# Windows (PowerShell)
$env:JD_COOKIE="你的完整Cookie"
$env:JD_DELIVERY_RECORD_IDS="3802615,3802616"
python refresh.py

# Linux / macOS
export JD_COOKIE="你的完整Cookie"
export JD_DELIVERY_RECORD_IDS="3802615,3802616"
python refresh.py
```

### 3. 配置 GitHub Actions 自动执行

#### 3.1 Fork 本仓库

点击右上角的 `Fork` 按钮，将仓库 Fork 到你的账号下。

#### 3.2 配置 Secrets

在你 Fork 的仓库中：

1. 进入 `Settings` → `Secrets and variables` → `Actions`
2. 点击 `New repository secret` 添加以下 Secrets：

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `JD_COOKIE` | 完整的 Cookie 字符串 | `3AB9D23F7A4B3CSS=...; __jda=...; __jdb=...` |
| `JD_DELIVERY_RECORD_IDS` | 投递记录 ID，多个用逗号分隔 | `3802615,3802616,3802617` |

#### 3.3 启用 Actions

1. 进入 `Actions` 标签页
2. 如果看到提示，点击 `I understand my workflows, go ahead and enable them`
3. 工作流将按照 `.github/workflows/refresh.yml` 中的定时任务执行

### 4. 定时执行时间

默认配置为每天北京时间 **09:00** 和 **21:00** 执行（8 小时冷却后可再次刷新）。

可以在 `.github/workflows/refresh.yml` 中修改 `cron` 表达式：

```yaml
schedule:
  - cron: '0 1,13 * * *'  # UTC 时间 01:00 和 13:00 (北京时间 09:00 和 21:00)
```

## 配置清单

在 GitHub Actions 中需要配置以下 Secrets：

### 必需配置

| 配置项 | 类型 | 说明 | 如何获取 |
|--------|------|------|---------|
| `JD_COOKIE` | Secret | 完整的 Cookie 字符串 | 浏览器开发者工具 → Application → Cookies → campus.jd.com |
| `JD_DELIVERY_RECORD_IDS` | Secret | 投递记录 ID 列表（逗号分隔） | 网络抓包或调用投递列表 API |

### Cookie 包含的关键字段（供参考）

- `3AB9D23F7A4B3CSS` - 会话认证
- `__jda` - 京东分析标识
- `__jdb` - 京东设备标识
- `__jdc` - 京东客户端标识
- `__jdu` - 京东用户标识
- `thor` - 雷神系统标识

## 注意事项

⚠️ **重要提示**：

1. **Cookie 有效期**：Cookie 可能会过期，如果脚本执行失败，请重新获取 Cookie 并更新 Secret
2. **刷新冷却时间**：京东规定刷新活跃度后需要等待 8 小时才能再次刷新
3. **请求频率**：脚本已内置请求间隔，避免请求过快导致封号
4. **隐私安全**：不要将 Cookie 泄露给他人，不要在公开场合分享
5. **合规使用**：本工具仅供学习交流使用，请遵守京东平台规则

## 手动触发

除了定时执行，你也可以手动触发刷新：

1. 进入仓库的 `Actions` 标签页
2. 选择 `京东校园招聘活跃度刷新` 工作流
3. 点击 `Run workflow` → `Run workflow`

## 日志查看

执行日志可以在 `Actions` 标签页中查看，每次执行都会显示：

- 执行时间
- 处理的投递记录数量
- 每条记录的检查和刷新结果
- 成功/失败统计

## 常见问题

### Q1: Cookie 如何获取？

A: 见上方"获取 Cookie"章节，使用浏览器开发者工具从 Application 标签页复制。

### Q2: 投递记录 ID 在哪里找？

A: 见上方"获取投递记录 ID"章节，通过网络抓包或 API 调用获取。

### Q3: 为什么执行失败？

A: 可能原因：
- Cookie 已过期，需重新获取
- 投递记录 ID 不正确
- 还在 8 小时冷却期内
- 网络问题

### Q4: 可以刷新多个投递记录吗？

A: 可以，在 `JD_DELIVERY_RECORD_IDS` 中用逗号分隔多个 ID，例如：`3802615,3802616,3802617`

### Q5: 如何修改执行时间？

A: 编辑 `.github/workflows/refresh.yml` 文件中的 `cron` 表达式。

## 许可证

MIT License

## 免责声明

本项目仅供学习交流使用，使用者需自行承担使用本工具的风险。作者不对使用本工具导致的任何后果负责。
