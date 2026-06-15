# ⚡ 快速开始指南

## 只需 3 步，5 分钟配置完成！

### 第 1 步：获取 Cookie（2 分钟）

**⚠️ 关键：必须复制所有 Cookie！**

1. Chrome 打开 https://campus.jd.com/ 并登录
2. 按 **F12** → **Application** → **Cookies** → **https://campus.jd.com**
3. **按 Ctrl+A 全选所有 Cookie** → **右键 → Copy**
4. 确保复制了所有 Cookie（通常有 30+ 个）

**重要**：如果只复制部分 Cookie 会导致 401 错误！

### 第 2 步：配置 GitHub Secret（2 分钟）

1. Fork 本仓库：https://github.com/MARYCOMPLEX/jd-refresh
2. 进入你的仓库 → **Settings** → **Secrets and variables** → **Actions**
3. 添加 1 个 Secret：

**Secret 名称**: `JD_COOKIE`  
**Secret 值**: 第 1 步获取的完整 Cookie

**就这一个！** 投递记录 ID 已经写死在代码中。

### 第 3 步：启用并测试（1 分钟）

1. 进入 **Actions** 标签页
2. 点击 **"I understand my workflows, go ahead and enable them"**
3. 选择 **"京东校园招聘活跃度刷新"** 工作流
4. 点击 **Run workflow** → **Run workflow** 手动测试
5. 查看日志确认成功 ✅

## 完成！🎉

脚本会自动在每天 **09:00** 和 **21:00**（北京时间）刷新简历活跃度。

---

## 📋 配置清单

- [ ] 获取 Cookie
- [ ] Fork 仓库
- [ ] 添加 `JD_COOKIE` Secret
- [ ] 启用 Actions
- [ ] 手动测试一次
- [ ] 查看日志确认成功

---

## ⚙️ 可选配置

### 修改执行时间

编辑 `.github/workflows/refresh.yml` 第 13 行：

```yaml
schedule:
  - cron: '0 1,13 * * *'  # 默认：北京时间 09:00 和 21:00
```

**常用时间**：
- `0 0,12 * * *` → 北京时间 08:00 和 20:00
- `0 2,14 * * *` → 北京时间 10:00 和 22:00

### 修改投递记录 ID

编辑 `refresh.py` 第 12 行：

```python
self.delivery_record_ids = [3802615]  # 修改为你的 ID
```

支持多个：
```python
self.delivery_record_ids = [3802615, 3802616, 3802617]
```

---

## 🆘 遇到问题？

- 📚 完整文档：查看 [README.md](README.md)
- 💬 提交 Issue：https://github.com/MARYCOMPLEX/jd-refresh/issues

---

## ⚡ 一句话总结

**获取 Cookie → 配置 Secret → 启用 Actions → 完成！**
