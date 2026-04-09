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

## 今日工作（2026-04-09 周四）

### ⏰ 当前时间：08:10 AM

### ✅ 2026-04-09 系统优化
- [x] 添加 1GB Swap 防止内存不足崩溃
- [x] 删除 cloudflared 释放 38MB
- [x] 优化 qmd 索引范围（限制只索引 memory 目录）
- [x] 主模型切换为 minimax/MiniMax-M2.7
- [x] Gateway 已重启生效


### ✅ 2026-04-08 21:47 待更新
- ⚠️ 钉钉发送失败问题（Send message failed）
- ✅ 小说创作：第21-28章已完成
- ✅ 规范流程制定完成

### ✅ 2026-04-08 已完成
- [x] Hermes Agent 安装和配置完成
- [x] DeepSeek API Key 配置（余额不足）
- [x] MiniMax-M2.5 模型配置成功 ✅
- [x] 自我进化记忆系统测试通过
- [x] 多模型架构验证完成
- [x] 技能系统测试通过（96个内置技能）
- [x] 工具调用功能验证
- [x] Hermes Gateway 服务启动成功
- [x] **定时任务功能测试通过** - 创建21个自动化工作流
- [x] **自动化工作流测试成功** - 链式工作流、智能工作流全部运行
- [x] **记忆系统集成验证** - MiniMax 记忆功能正常

### ⚠️ 待处理
- [ ] 加密货币 cron 脚本 PATH 问题
- [ ] 配置 Hermes 消息平台集成（钉钉/飞书）
- [ ] DeepSeek 充值后切换回 DeepSeek 模型
- [ ] OpenClaw 2026.4.8 安全审计（老大刚更新）

### ✅ 2026-04-08 18:11 已完成
- [x] 钉钉插件升级到 3.5.3 ✅
- [x] 钉钉配置修复（移除不支持的字段）
- [x] 钉钉恢复正常通信

### ✅ 2026-04-08 18:32 已完成
- [x] OpenClaw 更新到 2026.4.8 ✅
- [ ] 待执行：安全审计 `openclaw security audit`

### ✅ 2026-04-08 18:55 进行中
- [x] 老大询问新版本特性介绍 ✅
- [ ] 安全审计执行中


### ✅ 2026-04-08 模型状态
- [x] **MiniMax-M2.5**: ✅ 正常运行（当前主力）
- [ ] **DeepSeek**: ❌ 余额不足，需要充值

### ✅ 2026-04-08 工作流状态
- [x] **21个自动化工作流** 创建并运行中
- [x] Gateway 服务正常运行
- [x] 定时任务调度正常

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

## 钉钉插件自动修复脚本（2026-04-06）

### 创建原因
OpenClaw版本升级后，`plugin-sdk/telegram-core`模块被移除，导致钉钉插件加载失败。

### 脚本位置
`/home/admin/.openclaw/workspace/scripts/fix-dingtalk.sh`

### 使用方法
```bash
# 升级OpenClaw后运行:
bash /home/admin/.openclaw/workspace/scripts/fix-dingtalk.sh

# 然后重启Gateway:
openclaw gateway restart
```

### 原理
脚本自动检测并替换`channel.ts`中的旧import为兼容shim。
