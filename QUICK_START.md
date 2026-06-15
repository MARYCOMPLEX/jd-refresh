# ⚡ 快速开始指南

## 第 1 步：获取 Cookie（5 分钟）

1. Chrome 打开 https://campus.jd.com/ 并登录
2. 按 **F12** → **Application** → **Cookies** → **https://campus.jd.com**
3. 复制所有 Cookie（格式：`key1=value1; key2=value2; ...`）

## 第 2 步：验证 Cookie 并获取投递记录 ID（2 分钟）

```bash
# 克隆仓库
git clone https://github.com/MARYCOMPLEX/jd-refresh.git
cd jd-refresh

# 安装依赖
pip install -r requirements.txt

# 运行验证工具
python verify_cookie.py
```

输入你的 Cookie，工具会自动：
- ✅ 验证 Cookie 是否有效
- 📋 显示所有投递记录
- 💡 生成配置值（直接复制使用）

## 第 3 步：配置 GitHub Secrets（3 分钟）

1. Fork 仓库：https://github.com/MARYCOMPLEX/jd-refresh
2. 进入你的仓库 → **Settings** → **Secrets and variables** → **Actions**
3. 添加 2 个 Secrets：

### Secret 1: JD_COOKIE
- Name: `JD_COOKIE`
- Value: 第 1 步获取的完整 Cookie

### Secret 2: JD_DELIVERY_RECORD_IDS
- Name: `JD_DELIVERY_RECORD_IDS`
- Value: 第 2 步工具生成的 ID 列表（例如：`3802615,3802616`）

## 第 4 步：启用并测试（2 分钟）

1. 进入 **Actions** 标签页
2. 如果有提示，点击 **"I understand my workflows, go ahead and enable them"**
3. 选择 **"京东校园招聘活跃度刷新"** 工作流
4. 点击 **Run workflow** → **Run workflow** 手动测试
5. 查看日志确认成功 ✅

## 完成！🎉

现在脚本会自动在每天 **09:00** 和 **21:00**（北京时间）刷新你的简历活跃度。

---

## 📋 配置清单

- [ ] 获取 Cookie
- [ ] 运行 `verify_cookie.py` 验证
- [ ] Fork 仓库
- [ ] 添加 `JD_COOKIE` Secret
- [ ] 添加 `JD_DELIVERY_RECORD_IDS` Secret
- [ ] 启用 Actions
- [ ] 手动测试一次
- [ ] 查看日志确认成功

---

## 🆘 遇到问题？

- 📖 详细配置：查看 [SECRETS_CHECKLIST.md](SECRETS_CHECKLIST.md)
- 🔧 配置指南：查看 [CONFIG_GUIDE.md](CONFIG_GUIDE.md)
- 📚 完整文档：查看 [README.md](README.md)
- 💬 提交 Issue：https://github.com/MARYCOMPLEX/jd-refresh/issues

---

## ⚡ 一句话总结

**获取 Cookie → 验证有效性 → 配置 Secrets → 启用 Actions → 完成！**
