# GitHub Actions 配置清单

## 需要配置的 Secrets

在你的 GitHub 仓库中，进入 `Settings` → `Secrets and variables` → `Actions`，添加以下 Secrets：

### 1. JD_COOKIE

**说明**: 京东校园招聘的完整 Cookie 字符串

**如何获取**:
1. Chrome 浏览器打开 https://campus.jd.com/
2. 登录你的账号
3. 按 F12 打开开发者工具
4. 切换到 `Application` 标签页
5. 左侧展开 `Cookies` → `https://campus.jd.com`
6. 复制所有 Cookie（格式：`key1=value1; key2=value2; ...`）

**格式示例**:
```
3AB9D23F7A4B3CSS=ABC123...; __jda=123.456...; __jdb=789.012...; __jdc=campus_jd_com; __jdu=345678901; thor=ABCD1234...
```

**重要字段**（必须包含）:
- `3AB9D23F7A4B3CSS` - 会话凭证
- `__jda` - 京东分析
- `__jdb` - 京东标识
- `__jdc` - 京东客户端
- `__jdu` - 京东用户
- `thor` - 雷神标识

### 2. JD_DELIVERY_RECORD_IDS

**说明**: 投递记录 ID 列表，多个 ID 用英文逗号分隔

**如何获取**:

#### 方法一：浏览器开发者工具抓包（推荐）

1. 在京东校园招聘页面按 F12 打开开发者工具
2. 切换到 `Network` (网络) 标签页
3. 找到你已投递的职位
4. 点击"刷新活跃度"按钮
5. 在网络请求中找到 `checkCanResumeRefresh` 或 `refresh` 请求
6. 点击该请求，查看 `Payload` 或 `Request Body`
7. 其中的 `deliveryRecordId` 就是投递记录 ID

#### 方法二：调用 API 获取投递列表

使用 curl 或 Postman 调用以下 API：

**请求地址**: `https://campus.jd.com/api/wx/delivery/officialInfo/list`

**请求方法**: POST

**请求头**:
```
Cookie: 你的完整Cookie
Content-Type: application/json
```

**请求体**:
```json
{
  "pageNo": 1,
  "pageSize": 20
}
```

**curl 命令**:
```bash
curl -X POST 'https://campus.jd.com/api/wx/delivery/officialInfo/list' \
  -H 'Cookie: 你的完整Cookie' \
  -H 'Content-Type: application/json' \
  --data-raw '{"pageNo":1,"pageSize":20}'
```

返回的 JSON 中 `body.data.list` 数组中每个对象的 `deliveryRecordId` 字段就是投递记录 ID。

**格式示例**:
```
3802615,3802616,3802617
```

---

## 配置步骤

### 第 1 步：Fork 仓库

1. 访问 https://github.com/MARYCOMPLEX/jd-refresh
2. 点击右上角的 `Fork` 按钮
3. 等待 Fork 完成

### 第 2 步：添加 Secrets

1. 进入你 Fork 的仓库
2. 点击 `Settings`（设置）
3. 左侧菜单选择 `Secrets and variables` → `Actions`
4. 点击 `New repository secret`
5. 添加 `JD_COOKIE`：
   - Name: `JD_COOKIE`
   - Secret: 粘贴你的完整 Cookie
   - 点击 `Add secret`
6. 再次点击 `New repository secret`
7. 添加 `JD_DELIVERY_RECORD_IDS`：
   - Name: `JD_DELIVERY_RECORD_IDS`
   - Secret: 粘贴你的投递记录 ID（多个用逗号分隔）
   - 点击 `Add secret`

### 第 3 步：启用 Actions

1. 点击 `Actions` 标签页
2. 如果看到提示，点击 `I understand my workflows, go ahead and enable them`
3. 工作流已启用，将按计划自动执行

### 第 4 步：测试运行（可选）

1. 在 `Actions` 标签页中
2. 选择 `京东校园招聘活跃度刷新` 工作流
3. 点击 `Run workflow` 下拉菜单
4. 点击绿色的 `Run workflow` 按钮
5. 等待执行完成，查看日志确认是否成功

---

## 执行计划

默认配置为每天自动执行 2 次：
- 北京时间 09:00（UTC 01:00）
- 北京时间 21:00（UTC 13:00）

> 京东规定刷新活跃度后需要等待 8 小时才能再次刷新，因此设置为每 12 小时执行一次。

---

## 常见问题

### Q: Cookie 会过期吗？

A: 会的。如果发现脚本执行失败（返回 401 或其他认证错误），需要重新获取 Cookie 并更新 Secret。

### Q: 如何查看执行日志？

A: 进入 `Actions` 标签页，点击任意一次工作流运行记录，即可查看详细日志。

### Q: 可以修改执行时间吗？

A: 可以。编辑 `.github/workflows/refresh.yml` 文件中的 `cron` 表达式。注意使用 UTC 时间（北京时间 -8）。

### Q: 为什么有的投递记录刷新失败？

A: 可能原因：
- 该记录还在 8 小时冷却期内
- 投递记录 ID 不正确或已失效
- 该职位已下架或关闭投递

---

## 安全提示

⚠️ **重要**：
- 不要将 Cookie 分享给任何人
- 不要在公开场合展示你的 Cookie
- 定期更新 Cookie 以保证安全
- 如果怀疑 Cookie 泄露，立即修改密码并重新获取

---

## 技术支持

如有问题，请在 GitHub 仓库中提 Issue。
