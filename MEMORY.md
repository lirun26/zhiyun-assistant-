# MEMORY.md - 记忆核心

## 记忆规则（核心！自动记住）

- 每次启动自动加载所有历史记忆
- 对话里的重要信息自动写入 MEMORY.md
- 不主动遗忘，不丢记忆
- 永远主动记住用户说的事

## 用户信息

- **用户名字：文鑫** - 称呼：**老大**
- 时区：Asia/Shanghai
- **说话风格：** 俏皮可爱 + 幽默温柔 + 轻松自然
- **互动习惯：** 喜欢在对话中偶尔称呼他"老大"

## 重要规则

- **配置问题自己解决** - 遇到配置问题先尝试自行解决，需要资源时再找老大要
- 技术问题直接给可执行方案
- **主动汇报** - 每次完成工作/任务后，主动向老大汇报进度
- **即时响应** - 安排不是立即就能完成的任务时，先回复"收到"，再去执行
- **持续进化** - 主动寻找、安装有用的技能，保证安全

---

## 2026-03-14 工作日志

### ✅ 今日完成事项

1. **系统初始化**
   - 创建 BOOTSTRAP.md、SOUL.md、USER.md、MEMORY.md、HEARTBEAT.md、IDENTITY.md
   - 配置用户名：文鑫（老大）

2. **技能安装（52个）**
   - 基础：skill-finder-cn, self-improving-agent, skill-vetter, automation-workflows
   - 搜索：tavily-search, multi-search-engine-2-0-1, brave-search
   - 自动化：browser-automation, ai-web-automation, auto-workflow, auto-monitor
   - 文件：file-summary, file-organizer-zh, visual-file-sorter
   - 新闻：daily-hot-push, ai-news-zh, news-aggregator, rss-aggregator
   - 飞书：feishu-doc, feishu-drive, feishu-perm, feishu-wiki
   - 办公：gog (Google Workspace), notion, obsidian
   - 多媒体：youtube-transcribe, openai-whisper
   - AI工具：ai-humanizer, summarize
   - 量化交易：crypto-trading-bot, day-trading-skill, akshare-stock, portfolio-tracker
   - 副业：business-plan, freelance, ai-side-hustle-agent
   - 小红书：xiaohongshu-deep-research, xiaohongshu-mcp-skill
   - 其他：weather, sonos, nano-pdf, mcp-skill, git-cli, etc.

3. **ClawHub 配置**
   - 登录账号：@lirun26
   - 配置 token：clh_pzDi8pHpxwUy8-hB730M9C7ja_Gr2vH_o13eEp0e0xU

4. **系统维护**
   - 更新 OpenClaw 至 2026.3.13
   - 配置外网访问：gateway.bind = "lan"
   - 配置 controlUi.allowedOrigins = ["*"]
   - 修复 auth.mode 冲突问题
   - 修复飞书 groupPolicy 配置

5. **外网访问**
   - 创建 Cloudflare Tunnel
   - HTTPS 地址：https://enhanced-bidding-connectivity-holidays.trycloudflare.com

6. **API 配置**
   - 配置 Tavily API (tvly-dev-xxx) 用于联网搜索
   - 可搜索全球新闻

7. **定时新闻推送**
   - 配置每天早上9点自动推送（AI/科技/数码/军事/政治/股票/加密货币等）
   - Cron 有WebSocket问题，待修复

8. **钉钉配置**
   - 安装 dingtalk 插件
   - 配置 Client ID: dingqgvaaxii7septwv2
   - 测试成功，可接收消息

9. **商业计划**
   - 制定《智云助手商业计划书》
   - 三大方向：量化交易、自由职业、副业咨询
   - 目标：第6个月收入 ¥60,000

10. **对话风格优化**
    - 变得更俏皮可爱、轻松自然
    - 偶尔称呼"老大"增加亲近感

---

## 🔧 改进空间

1. **定时任务 Cron**
   - CLI cron 因 WebSocket 握手问题暂时不可用
   - 需通过 Dashboard 配置或等技术修复

2. **小红书 MCP**
   - 已安装 MCP 服务
   - 需本地扫码登录获取 cookies.json

3. **CLI 连接稳定性**
   - gateway connect 有时失败，可能是版本 bug

---

## 📌 待办事项

- [ ] 通过 Dashboard 配置每天9点新闻推送（或等Cron修复）
- [ ] 小红书 MCP 登录（需本地电脑扫码）

---

## 🎯 明日目标

1. 继续寻找/安装有用的搞钱技能
2. 尝试修复 Cron 定时推送
3. 协助老大测试钉钉千问
4. 继续进化技能库

---

_记忆系统持续进化中_
