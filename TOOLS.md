# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## 小说创作流程（2026-04-01 新增，必须严格遵守）

### ⚠️ 写小说必须调用的4个技能步骤

**每次创作新章节前，必须按顺序执行：**

1. **【读取skill指导】**
   - 读取 `open-novel-writing` 或 `novel-generator` 的SKILL.md
   - 获取写作规范和质量标准

2. **【章节规划（spec生成）】**
   - 先基于前3章生成章节规格（spec）
   - 检查人物状态、场景位置、伏笔一致性
   - 连贯性检查通过后才开始写

3. **【评审反馈（自检P0/P1）】**
   - 写完后对照P0/P1红线自检：
   - P0绝对禁止：AI词汇、感悟式结尾、感叹式结尾、上帝视角
   - P1建议避免：套路化表达、流水账、抽象心理
   - 评分≥85分才合格

4. **【更新记忆文件】**
   - 新角色 → 记录到 `.learnings/CHARACTERS.md`
   - 角色状态变化 → 更新对应角色条目
   - 新地点 → 记录到 `.learnings/LOCATIONS.md`
   - 关键情节 → 记录到 `.learnings/PLOT_POINTS.md`
   - 失败/问题 → 记录到 `.learnings/ERRORS.md`

### 文件结构（小说项目）
```
novels/仙帝重修录/
├── 第XX章_章节名.md    # 已发送的章节
├── .learnings/         # 记忆系统（跨session连续性）
│   ├── CHARACTERS.md   # 角色状态追踪
│   ├── LOCATIONS.md    # 地点追踪
│   ├── PLOT_POINTS.md  # 情节追踪
│   ├── STORY_BIBLE.md  # 世界观设定
│   └── ERRORS.md       # 失败记录
└── output/            # 输出目录（可选）
```

### 评审维度（5角色评分）
| 角色 | 关注点 | 权重 |
|:---|:---|:---|
| 阅读者 | 开篇吸引力、节奏、画面感 | 25% |
| 编审 | 错别字、病句、一致性 | 25% |
| 故事家 | 剧情逻辑、伏笔、钩子 | 25% |
| 文学顾问 | 语言艺术、人物刻画 | 15% |
| 毒舌读者 | 套路化、水文、毒点 | 10% |

### 评分标准
- 90-100：精品
- 85-89：优秀，可发布
- 75-84：良好，小改可发
- 60-74：合格，需修改
- 60以下：不合格，重写

---

## OpenClaw WebUI 外部网络访问配置

### 需求
让 WebUI 能够从外部网络（如阿里云服务器）访问

### 配置步骤

1. **设置 basePath**（8位随机字符串，增加安全性）
   ```bash
   openclaw config set gateway.controlUi.basePath <随机8位字符>
   ```

2. **设置允许的来源地址**
   ```bash
   openclaw config set gateway.controlUi.allowedOrigins '["http://你的公网IP:18789"]'
   ```

3. **允许非安全认证**（可选，用于调试）
   ```bash
   openclaw config set gateway.controlUi.allowInsecureAuth true
   ```

4. **禁用设备认证**（可选，用于开放访问）
   ```bash
   openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true
   ```

5. **重启 Gateway**
   ```bash
   openclaw gateway restart
   ```

### 访问方式
- 内部访问：`http://127.0.0.1:18789`
- 外部访问：`http://<公网IP>:18789/<basePath>`

### 注意事项
- `dangerouslyDisableDeviceAuth` 会禁用设备配对认证，生产环境谨慎使用
- 建议使用强 token 和 IP 白名单限制访问

---

---

## Beads（任务追踪）

- **安装**: `curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash`
- **版本**: v0.63.3
- **用途**: AI Agent 分布式图结构任务追踪器
- **位置**: `/home/admin/.local/bin/bd`
- **仓库**: `.beads/` 目录（已 git 关联）

### 常用命令
```bash
bd init              # 初始化项目
bd create "标题" -p 0  # 创建任务（P0=最高优先级）
bd list             # 列出所有任务
bd ready           # 显示可执行的任务
bd dep add <child> <parent>  # 添加依赖
bd show <id>       # 查看任务详情
bd update <id> --claim  # 领取任务
bd close <id>      # 关闭任务
```

### 当前任务
- workspace-2dn: 集成 Beads 到自我进化系统 (P1)
- workspace-vwg: 测试 Beads 任务系统 (P2)

---

## XCrawl（网页抓取）

- **API Key**: xc-OZ2VkcRwvGNBLwBjxU4njKBxCZNxmsW3JBwTz60s3RsTBU9R
- **文档**: https://docs.xcrawl.com
- **SDK**: pip install xcrawl-py

Add whatever helps you do your job. This is your cheat sheet.
