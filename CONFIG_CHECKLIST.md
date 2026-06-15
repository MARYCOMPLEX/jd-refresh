# 📋 京东校园招聘自动刷新 - 配置清单

## ✅ 项目信息

- **仓库地址**: https://github.com/MARYCOMPLEX/jd-refresh
- **功能**: 自动刷新京东校园招聘简历活跃度
- **默认执行时间**: 每天北京时间 09:00 和 21:00

---

## 🎯 只需配置 1 个 Secret

### JD_COOKIE（必需）

**说明**: 京东校园招聘的完整 Cookie 字符串

**获取步骤**:
1. Chrome 浏览器打开 https://campus.jd.com/ 并登录
2. 按 **F12** → **Application** → **Cookies** → **https://campus.jd.com**
3. 复制所有 Cookie

**配置位置**:  
GitHub 仓库 → `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

**Secret 名称**: `JD_COOKIE`  
**Secret 值**: 完整的 Cookie 字符串

**格式示例**:
```
3AB9D23F7A4B3CSS=ABC123...; __jda=123.456...; __jdb=789...; __jdc=campus_jd_com; __jdu=345678901; thor=ABCD...
```

**必须包含的关键字段**:
- `3AB9D23F7A4B3CSS` - 会话认证（最重要）
- `__jda`, `__jdb`, `__jdc`, `__jdu` - 京东标识
- `thor` - 雷神系统标识

---

## ⚙️ 可选配置（直接修改代码）

### 1. 修改投递记录 ID

**文件**: `refresh.py`  
**位置**: 第 12 行

**默认值**:
```python
self.delivery_record_ids = [3802615]
```

**支持多个 ID**:
```python
self.delivery_record_ids = [3802615, 3802616, 3802617]
```

### 2. 修改执行时间

**文件**: `.github/workflows/refresh.yml`  
**位置**: 第 13 行

**默认值** (北京时间 09:00 和 21:00):
```yaml
schedule:
  - cron: '0 1,13 * * *'
```

**常用时间对照表**:

| UTC 时间 | 北京时间 | cron 表达式 |
|---------|---------|------------|
| 00:00, 12:00 | 08:00, 20:00 | `0 0,12 * * *` |
| 01:00, 13:00 | 09:00, 21:00 | `0 1,13 * * *` (默认) |
| 02:00, 14:00 | 10:00, 22:00 | `0 2,14 * * *` |

---

## 🚀 快速配置流程

### 第 1 步：Fork 仓库
访问 https://github.com/MARYCOMPLEX/jd-refresh 点击 **Fork**

### 第 2 步：获取 Cookie
Chrome 打开京东校园招聘 → F12 → Application → Cookies → 复制

### 第 3 步：配置 Secret
仓库 → Settings → Secrets and variables → Actions → 添加 `JD_COOKIE`

### 第 4 步：启用 Actions
Actions 标签页 → 启用工作流 → 手动运行一次测试

---

## ✅ 完成检查清单

- [ ] Fork 了仓库
- [ ] 获取了完整的 Cookie
- [ ] 添加了 `JD_COOKIE` Secret
- [ ] 启用了 GitHub Actions
- [ ] 手动测试执行成功
- [ ] 查看日志确认无误

---

## 🔍 验证功能

脚本首次运行时会**自动验证 Cookie 是否有效**：
- ✅ Cookie 有效 → 继续执行刷新
- ❌ Cookie 无效 → 停止执行并提示重新获取

---

## ⏰ 执行逻辑

1. **首次验证**: 调用投递列表 API 验证 Cookie 有效性
2. **检查刷新**: 对每个投递记录检查是否可以刷新
3. **执行刷新**: 如果可以刷新，则执行刷新操作
4. **统计结果**: 输出成功/失败统计

---

## ⚠️ 注意事项

1. **Cookie 有效期**: 通常几天到几周会过期，需定期更新
2. **刷新限制**: 刷新后需等待 8 小时才能再次刷新
3. **Cookie 安全**: 不要分享给任何人，不要公开展示
4. **合规使用**: 仅供学习交流，请遵守平台规则

---

## 📊 执行日志示例

```
============================================================
🚀 京东校园招聘活跃度刷新任务
⏰ 执行时间: 2026-06-16 09:00:00
============================================================

🔍 验证 Cookie 有效性...
✅ Cookie 有效！

📋 待刷新的投递记录数量: 1

[1/1] 处理投递记录: 3802615
  检查结果: {"success":true,"body":{"canRefresh":true}}
  刷新结果: {"success":true,"body":{"noticeMsg":"简历已成功置顶！在8小时后可以再次刷新活跃度～"}}
  ✅ 简历已成功置顶！在8小时后可以再次刷新活跃度～

============================================================
📊 执行结果统计:
  ✅ 成功: 1
  ❌ 失败: 0
  📝 总计: 1
============================================================
```

---

## 🆘 常见问题

### Q: Cookie 从哪里获取？
A: Chrome 浏览器 → F12 → Application → Cookies → campus.jd.com

### Q: Cookie 多久会过期？
A: 通常几天到几周，如果脚本失败，重新获取即可

### Q: 如何修改执行时间？
A: 编辑 `.github/workflows/refresh.yml` 第 13 行的 cron 表达式

### Q: 如何修改投递记录 ID？
A: 编辑 `refresh.py` 第 12 行的 `delivery_record_ids` 列表

### Q: 为什么显示"还在冷却期内"？
A: 正常现象，刷新后需等待 8 小时才能再次刷新

---

## 📞 获取帮助

- GitHub Issues: https://github.com/MARYCOMPLEX/jd-refresh/issues
- 查看完整文档: [README.md](README.md)
- 快速开始: [QUICK_START.md](QUICK_START.md)
