# 京东校园招聘自动刷新活跃度

自动刷新京东校园招聘平台的简历活跃度，保持投递记录的曝光度。

## 功能特性

- ✅ 自动检查是否可以刷新活跃度
- ✅ 自动执行简历刷新操作
- ✅ GitHub Actions 定时自动执行
- ✅ 详细的执行日志和结果统计
- ✅ 仅需配置 Cookie，其他参数已写死在代码中

## 快速开始

### 1. 获取 Cookie

1. 使用 Chrome 浏览器打开 [京东校园招聘](https://campus.jd.com/)
2. 登录你的账号
3. 按 `F12` 打开开发者工具
4. 切换到 `Application` 标签页（或 `应用` 标签页）
5. 左侧展开 `Cookies` → `https://campus.jd.com`
6. 复制所有 Cookie（格式：`key1=value1; key2=value2; ...`）

**重要的 Cookie 字段**（至少需要这些）：
- `3AB9D23F7A4B3CSS` - 会话凭证（最重要）
- `__jda` - 京东分析
- `__jdb` - 京东标识
- `__jdc` - 京东客户端
- `__jdu` - 京东用户
- `thor` - 雷神标识

### 2. Fork 仓库并配置 Secret

1. 点击右上角的 `Fork` 按钮，将仓库 Fork 到你的账号下
2. 进入你 Fork 的仓库
3. 进入 `Settings` → `Secrets and variables` → `Actions`
4. 点击 `New repository secret` 添加以下 Secret：

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `JD_COOKIE` | 完整的 Cookie 字符串 | `3AB9D23F7A4B3CSS=...; __jda=...; __jdb=...` |

**就这一个配置！** 投递记录 ID 已经写死在代码中（`refresh.py` 第 12 行）。

### 3. 启用 Actions

1. 进入 `Actions` 标签页
2. 如果看到提示，点击 `I understand my workflows, go ahead and enable them`
3. 工作流将按照配置的定时任务执行

### 4. 调整执行时间（可选）

默认配置为每天北京时间 **09:00** 和 **21:00** 执行（8 小时冷却后可再次刷新）。

如需修改执行时间，编辑 `.github/workflows/refresh.yml` 文件第 13 行的 `cron` 表达式：

```yaml
schedule:
  - cron: '0 1,13 * * *'  # UTC 时间（北京时间 -8）
```

**常用时间对照表**：

| UTC 时间 | 北京时间 | cron 表达式 |
|---------|---------|------------|
| 01:00 | 09:00 | `0 1 * * *` |
| 13:00 | 21:00 | `0 13 * * *` |
| 00:00 | 08:00 | `0 0 * * *` |
| 12:00 | 20:00 | `0 12 * * *` |
| 02:00 | 10:00 | `0 2 * * *` |
| 14:00 | 22:00 | `0 14 * * *` |

**示例**：如果想在每天早上 8 点和晚上 8 点执行，修改为：
```yaml
schedule:
  - cron: '0 0,12 * * *'
```

### 5. 修改投递记录 ID（可选）

如果需要刷新其他投递记录，编辑 `refresh.py` 第 12 行：

```python
self.delivery_record_ids = [3802615]  # 修改为你的投递记录 ID
```

支持多个 ID：
```python
self.delivery_record_ids = [3802615, 3802616, 3802617]
```

## 本地测试

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
python refresh.py

# Linux / macOS
export JD_COOKIE="你的完整Cookie"
python refresh.py
```

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

## 配置清单

在 GitHub Actions 中需要配置的 Secret：

### 必需配置

| 配置项 | 类型 | 说明 | 如何获取 |
|--------|------|------|---------|
| `JD_COOKIE` | Secret | 完整的 Cookie 字符串 | 浏览器开发者工具 → Application → Cookies → campus.jd.com |

### 可选配置（直接修改代码）

| 配置项 | 位置 | 说明 |
|--------|------|------|
| 投递记录 ID | `refresh.py` 第 12 行 | 需要刷新的投递记录 ID 列表 |
| 执行时间 | `.github/workflows/refresh.yml` 第 13 行 | 定时执行的 cron 表达式 |

## 注意事项

⚠️ **重要提示**：

1. **Cookie 有效期**：Cookie 可能会过期，如果脚本执行失败，请重新获取 Cookie 并更新 Secret
2. **刷新冷却时间**：京东规定刷新活跃度后需要等待 8 小时才能再次刷新
3. **请求频率**：脚本已内置请求间隔，避免请求过快导致封号
4. **隐私安全**：不要将 Cookie 泄露给他人，不要在公开场合分享
5. **合规使用**：本工具仅供学习交流使用，请遵守京东平台规则

## 许可证

MIT License

## 免责声明

本项目仅供学习交流使用，使用者需自行承担使用本工具的风险。作者不对使用本工具导致的任何后果负责。
