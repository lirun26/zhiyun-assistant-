# HEARTBEAT.md - 主动性任务

# 保持主动，但不打扰

---

## 🧬 自我进化系统 v2（2026-04-01 启用）

### ✅ 已配置定时任务
| 任务 | 时间 | Cron |
|:---|:---|:---|
| 每日自我复盘v2 | 18:00 | `0 0 18 * * *` |
| 每日进化早报v2 | 08:00 | `0 0 8 * * *` |

### 🔧 整合的进化引擎
| 引擎 | 功能 |
|:---|:---|
| ai-evolution-engine-v2 | 每日评估 + 进化 |
| actual-self-improvement | 错误记录 + 学习记录 |
| auto-skill-evolver | 技能优化提案 |

### 📁 快速命令
```bash
bash skills/self-review/scripts/quick_evolve.sh status
```

### 📊 进化数据
- 进化日志：`memory/evolution/YYYY-MM-DD.md`
- 学习记录：`.learnings/LEARNINGS.md`
- 错误记录：`.learnings/ERRORS.md`

---

## 今日工作（2026-04-01 周三）

### ✅ 2026-04-01 完成
- [x] 加密货币早报自动发送成功（BTC $68,337 / ETH $2,113）
- [x] 钉钉推送成功

### ⚠️ 待处理
- [ ] 加密货币 cron 脚本 PATH 问题（openclaw 命令找不到）

---

### ✅ 2026-03-30 完成
- [x] 磁盘清理：释放 12.5G（uv缓存7.6G + pip缓存3G + Docker镜像1.9G）
- [x] 安装 slavingia/skills（10个极客企业家技能）
- [x] 分析 OpenClaw 2026.3.28 新功能
- [x] 记忆文件更新（HOT_MEMORY.md, 2026-03-29.md）

---

## 提醒老大的事项

⚠️ **小红书MCP登录**
- 需要在本地电脑运行 xiaohongshu-login 扫码登录
- 登录后生成 cookies.json，复制到服务器 /tmp/

⚠️ **dream-to-video 暂停**
- 即梦"Agent模式"与"视频生成"模式不同，代码卡在Agent模式
- 老大说"即梦有钱"，考虑付费方案

---

## 📋 待办任务（2026-03-30）

### Tolink 机场配置
- **内容**：配置 lan-proxy-gateway + Tolink 订阅
- **状态**：等待订阅链接
- **已完成**：gateway 和 mihomo 已安装
- **待完成**：老大购买后提供订阅链接

---

## ⏰ 定时任务
- **明天18:00提醒**：Lark CLI 授权配置（运行 lark-cli config init）

## 主动性提醒

- 记住老大习惯：喜欢测试，对技术感兴趣
- 定期检查系统健康状态
- **完成任务后主动汇报老大**
- **持续进化技能库**

---

## 🐵 阿里悟空待办

- 官网：https://www.dingtalk.com/wukong
- 等API开放后做"悟空Skill"封装

---

## 📤 Clawhub 已发布

- multi-search-aggregator（2026-03-26）

---

## 📈 加密货币定时监控

- 每日 9:00 自动执行
- 脚本：`/home/admin/.openclaw/workspace/crypto-bot/daily_report.py`

---

## ⚠️ 插件更新审计

老大要求：插件更新时执行 `openclaw security audit`

---

_智云助手 2026-03-31 凌晨_
