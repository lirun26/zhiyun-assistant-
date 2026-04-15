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

## 小说创作流程（番茄签约版 v6）

### ⚠️ 每次创作新章节前，必须严格按以下步骤执行：

#### 第1步：读取skill指导
- 读取 `skills/linfeng-novel/SKILL.md`（番茄签约核心规范）
- 读取 `open-novel-writing` 的SKILL.md（基础写作规范）
- 读取 `ai-novel-writing-assistant` 的SKILL.md（AI辅助工具）

#### 第2步：AI辅助章节规划
```bash
# 检查服务状态
curl -s http://localhost:3000/api/novels | jq .data.items[0].id

# 在Creative Hub中生成章节spec
curl -s -N -X POST "http://localhost:3000/api/creative-hub/threads/{threadId}/runs/stream" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"type": "human", "content": "基于前3章剧情，生成第X章章节规格"}], "provider": "siliconflow", "model": "Qwen/Qwen2.5-7B-Instruct"}'
```

#### 第3步：创作正文
- 按spec创作，确保**2500-3500字**（上限3500，禁止超）
- 开篇公式：第1句→事件冲突；前3段→主角身份；前1页→第一个冲突
- 禁止P0红线

#### 第4步：创建评审报告（必须执行）
| 检查项 | 内容 |
|:---|:---|
| 字数统计 | wc -m 确认**2500-3500字** |
| 开篇检查 | 第1句是否有事件冲突，不是环境描写 |
| AI味检测 | 详见下方AI味识别清单 |
| 逻辑检查 | 资金/物品/交通前后一致 |
| 时间线检查 | 无矛盾 |

#### 🚫 AI味识别清单（每章必检）
```
[ ] 无"本章总结/下章预告"段落
[ ] 无"绝非...绝不...绝不再..."排比句式
[ ] 无连续3段以上内心独白
[ ] 主角性格通过行动展示，不是独白宣告
[ ] 每件物品"先出现再使用"
[ ] 固定句式（如"嘴角勾起一抹..."）出现不超2次/章
```

**重复描写检查**：
- 同一事物在前文已描写过，后文再次描写必须换词
- 同类情节表述不能雷同（检查前3章）
- 检查关键词："羊脂白玉/温润/流年不利/让我等等"等

**章节结尾对比检查**（必须执行）：
- 用grep检查前3章结尾关键词
- 禁止重复："一步步走下去/清算的开始/灵力流转/等他xxx"等
- 每章结尾必须独一无二，表达方式不同

**章节开头对比检查**（必须执行）：
- 检查前3章开头场景模式
- 禁止相同地点+时间+人物状态的组合（如"老城区+夜色+修炼"）
- 每章开头必须有差异化（地点/时间/氛围/人物状态）

**章节中间整段重复检查**（必须执行）：
- 用grep -n "当晚\|突然\|这时" 检查是否有整段重复
- 检查相邻段落是否有完全相同的句子

**章节名检查**（必须执行）：
- 章节名必须准确反映本章核心事件
- 禁止章节名与内容不符

**禁止重复情节检查**（必须执行）：
- 禁止与前文重复的情节模式（如：修炼→醒来→制定计划这种固定流程）
- 每章核心事件必须不同，场景/时间/人物状态必须有新意

**禁止修仙术语检查**（必须执行）：
- 都市/风水商战类：禁止炼气境/金丹期/筑基/元婴/化神等
- 必须与小说类型匹配：都市用都市体系（道行/功底/造诣），修仙用修仙体系，不能混乱

#### 第5步：修正问题
- 按评审结果修正问题
- 修正后重新检查

#### 第6步：33维度审计
- 执行33维度审计（见下方审计系统）
- 每章必须通过33项检查
- 审计报告保存到 `.learnings/AUDIT/第XX章_审计报告.md`
- 33项全部通过才能发送

#### 第7步：更新记忆文件
- 新角色 → `.learnings/CHARACTERS.md`
- 角色状态变化 → 更新对应角色条目
- 新地点 → `.learnings/LOCATIONS.md`
- 关键情节 → `.learnings/PLOT_POINTS.md`
- 章节摘要 → `.learnings/CHAPTERS.md`
- 新埋伏笔 → `.learnings/HOOKS.md`
- 物品获取/消耗 → `.learnings/ITEMS.md`
- 失败/问题 → `.learnings/ERRORS.md`

#### 第8步：发送（只发标题+正文）

#### 第8步：发送（只发标题+正文）
- 邮件标题：《书名》第XX章 章节标题
- 邮件正文：只放章节正文，无附件无分隔线

### 文件结构（小说项目）
```
novels/天机风水商途/
├── 第XX章_章节名.md    # 已发送的章节
├── .learnings/         # 记忆系统（跨session连续性）
│   ├── CHARACTERS.md   # 角色状态追踪
│   ├── LOCATIONS.md   # 地点追踪
│   ├── PLOT_POINTS.md # 情节追踪
│   ├── CHAPTERS.md    # 章节摘要
│   ├── HOOKS.md       # 伏笔追踪
│   ├── ITEMS.md       # 物资追踪
│   ├── FENG_SHUI_KNOWLEDGE.md  # ⭐风水知识库（必读）
│   ├── STORY_BIBLE.md # 世界观设定
│   └── ERRORS.md      # 失败记录
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

## 🚨 强制评审Checklist（每章必查）

### 发前必查项目（逐项打勾）

```
[ ] 1. 字数检查：wc -m ≥ 4000
[ ] 2. P0红线检查：
      - 无"赋能/维度/赛道"等AI词汇
      - 无感悟式/感叹式结尾
      - 无上帝视角叙述
[ ] 3. 修仙术语检查：
      - grep "炼气\|金丹\|筑基\|元婴\|化神" → 必须无
      - grep "灵力\|修为" → 确认上下文为都市风水用语
[ ] 4. 姓氏一致性检查：
      - grep "叶家\|叶氏" → 必须无（应为顾家/顾氏）
[ ] 5. 重复表达检查：
      - grep "微微一笑\|嘴角微微上扬\|露出一抹淡淡的笑容" → 同一角色不超过2次
      - grep "淡淡的笑容" → 检查前3章是否有相同表达
[ ] 6. 结尾对比：
      - tail -5 检查本章结尾
      - grep 前3章结尾关键词 → 确保不雷同
[ ] 7. 开头对比：
      - head -10 检查本章开头
      - 确认地点/时间/人物状态与前3章不雷同
[ ] 8. 章节名检查：
      - 章节名是否准确反映本章核心事件
[ ] 9. 逻辑检查：
      - 人物位置是否连贯
      - 人物状态是否合理（受伤→痊愈等）
      - ⚠️ 角色认知逻辑：反派/配角的台词是否超出该角色认知范围
[ ] 10. AI味检测：
      - grep "突然" | wc -l → 出现次数过多说明句式单调
      - grep "就在这时" → 典型AI连接词，应删除
      - grep "不得不" | wc -l → 出现3次以上说明表达单一
      - 检查是否有"首先/其次/最后"等机械连接词
[ ] 11. 发送前再读一遍结尾
```

### 伏笔回收检查
- 每章创作前检查 `.learnings/HOOKS.md` 中待回收伏笔
- 新埋伏笔后更新 `HOOKS.md`
- 回收伏笔时引用原始场景原文

### 物资追踪检查
- 物品获取/丢失后更新 `.learnings/ITEMS.md`
- 战力变化后更新境界上限

### 每章摘要更新
- 章节发送后更新 `.learnings/CHAPTERS.md`
- 记录：章节号、标题、核心事件、字数

### 执行命令（番茄签约版）

```bash
# 快速检查（发前必跑）
echo "=== 字数检查(2500-3500) ===" && wc -m 第XX章*.md
echo "=== AI味检测 ===" && grep -c "总结\|预告\|绝非\|绝不" 第XX章*.md || echo "无 ✅"
echo "=== 固定句式检测 ===" && grep -c "嘴角勾起一抹" 第XX章*.md
echo "=== 结尾检查 ===" && tail -5 第XX章*.md
echo "=== 开篇检查 ===" && head -10 第XX章*.md
```

### 评审标准
- 字数2500-3500 ✅ → 可发送
- 字数2000-2500 → 需补内容
- 字数<2000 → 禁止发送
- AI味检测全通过 → 可发送

### 评审标准
- 10项全部通过 → 可发送
- 任意1项不通过 → 必须修正后再发送
- 5项以上不通过 → 重新创作

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

## 📚 AI提示词资源（2026-04-10 新增）

### Prompts
- **prompts.chat** — AI Prompts 社区平台，分享/发现/收藏提示词，开源可自托管
  - https://prompts.chat/


---

## 📊 33维度审计系统

### 审计流程
每章创作完成后，必须执行33维度审计。

### 33维度清单

#### A. 角色维度（5个）
| ID | 维度 | 检查方法 |
|:---:|:---|:---|
| A1 | 角色记忆 | 角色不能"记起"从未亲眼见过的事 |
| A2 | 角色状态 | 当前位置、情绪、体力必须一致 |
| A3 | 角色能力 | 技能使用不能超出当前境界 |
| A4 | 角色关系 | 对话态度必须符合关系亲疏 |
| A5 | 角色成长 | 性格变化必须有铺垫 |

#### B. 连续性维度（6个）
| ID | 维度 | 检查方法 |
|:---:|:---|:---|
| B1 | 时间线 | grep 日期/时间词，确认顺序正确 |
| B2 | 地点 | 角色位置必须连贯 |
| B3 | 物品 | 物品获取/消耗必须有记录 |
| B4 | 天气/环境 | 不能前后矛盾 |
| B5 | 势力分布 | 各势力位置不能冲突 |
| B6 | 资源数量 | 金钱/物资不能超出已有 |

#### C. 伏笔维度（4个）
| ID | 维度 | 检查方法 |
|:---:|:---|:---|
| C1 | 伏笔埋设 | 每章最多2个新伏笔 |
| C2 | 伏笔回收 | 必须引用原始场景 |
| C3 | 伏笔逻辑 | 回收必须有因果关系 |
| C4 | 钩子设置 | 章节结尾必须有钩子 |

#### D. 叙事维度（5个）
| ID | 维度 | 检查方法 |
|:---:|:---|:---|
| D1 | 节奏 | 高潮→缓冲→发展循环 |
| D2 | 信息密度 | 不能流水账 |
| D3 | 冲突设计 | 每章必须有核心冲突 |
| D4 | 悬念 | 关键信息延迟释放 |
| D5 | 视角 | 不能突然切换视角 |

#### E. 语言维度（5个）
| ID | 维度 | 检查方法 |
|:---:|:---|:---|
| E1 | AI词汇 | 无"赋能/维度/赛道"等 |
| E2 | 句式单调 | "突然/就在这时"出现过多 |
| E3 | 感悟式结尾 | 禁止总结式/感悟式结尾 |
| E4 | 感叹式结尾 | 禁止感叹号结尾 |
| E5 | 重复表达 | 同一描写不超2次 |

#### F. 逻辑维度（4个）
| ID | 维度 | 检查方法 |
|:---:|:---|:---|
| F1 | 因果逻辑 | 事件必须有因果 |
| F2 | 战力逻辑 | 越级挑战必须有原因 |
| F3 | 情报逻辑 | 获取情报必须有来源 |
| F4 | 动机逻辑 | 角色行为必须有动机 |

#### G. 类型维度（4个）
| ID | 维度 | 检查方法 |
|:---:|:---|:---|
| G1 | 修仙术语 | 都市类禁止修仙用语 |
| G2 | 都市术语 | 修仙类禁止现代用语 |
| G3 | 设定一致 | 境界体系不能混乱 |
| G4 | 地理真实 | 地名/距离必须合理 |

### 审计执行命令

```bash
# 33维度审计命令
echo "=== A.角色维度 ==="
# A1-A5 需要人工检查

echo "=== B.连续性维度 ==="
grep -n "当晚\|次日\|第三天" 第XX章*.md  # B1时间线
grep -n "突然\|就在这时" 第XX章*.md | wc -l  # E2句式单调

echo "=== C.伏笔维度 ==="
# 检查 HOOKS.md

echo "=== D.叙事维度 ==="
tail -3 第XX章*.md  # D4钩子

echo "=== E.语言维度 ==="
grep -n "赋能\|维度\|赛道" 第XX章*.md || echo "无AI词汇 ✅"
grep -n "微微一笑\|淡淡的笑容" 第XX章*.md | wc -l

echo "=== F.逻辑维度 ==="
# 人工检查

echo "=== G.类型维度 ==="
grep -n "炼气\|金丹\|筑基\|灵力\|修为" 第XX章*.md || echo "无修仙术语 ✅"
grep -n "叶家\|叶氏" 第XX章*.md || echo "无姓氏错误 ✅"
```

### 审计报告模板

```markdown
## 第XX章审计报告

| 维度 | 状态 | 问题 |
|:---|:---:|:---|
| A1 角色记忆 | ✅/❌ | |
| A2 角色状态 | ✅/❌ | |
| A3 角色能力 | ✅/❌ | |
| A4 角色关系 | ✅/❌ | |
| A5 角色成长 | ✅/❌ | |
| B1 时间线 | ✅/❌ | |
| B2 地点 | ✅/❌ | |
| B3 物品 | ✅/❌ | |
| B4 环境 | ✅/❌ | |
| B5 势力 | ✅/❌ | |
| B6 资源 | ✅/❌ | |
| C1 伏笔埋设 | ✅/❌ | |
| C2 伏笔回收 | ✅/❌ | |
| C3 伏笔逻辑 | ✅/❌ | |
| C4 钩子 | ✅/❌ | |
| D1 节奏 | ✅/❌ | |
| D2 信息密度 | ✅/❌ | |
| D3 冲突 | ✅/❌ | |
| D4 悬念 | ✅/❌ | |
| D5 视角 | ✅/❌ | |
| E1 AI词汇 | ✅/❌ | |
| E2 句式单调 | ✅/❌ | |
| E3 感悟式结尾 | ✅/❌ | |
| E4 感叹式结尾 | ✅/❌ | |
| E5 重复表达 | ✅/❌ | |
| F1 因果逻辑 | ✅/❌ | |
| F2 战力逻辑 | ✅/❌ | |
| F3 情报逻辑 | ✅/❌ | |
| F4 动机逻辑 | ✅/❌ | |
| G1 修仙术语 | ✅/❌ | |
| G2 都市术语 | ✅/❌ | |
| G3 设定一致 | ✅/❌ | |
| G4 地理真实 | ✅/❌ | |

**总分**：__/33 通过
**结论**：✅ 可发送 / ❌ 需修改
```

---


## 🧬 自我进化系统

### 核心Skill（已集成）
```bash
# 进化状态检查
bash skills/self-review/scripts/quick_evolve.sh status

# 技能自检
bash skills/auto-skill-evolver/scripts/self_check.sh

# 每日热榜推送
bash skills/daily-hot-push/push.sh
```

### 进化数据位置
- 进化日志：`memory/evolution/YYYY-MM-DD.md`
- 学习记录：`.learnings/LEARNINGS.md`
- 错误记录：`.learnings/ERRORS.md`

### 定时任务
| 任务 | Cron | 功能 |
|:---|:---|:---|
| 每日自我复盘 | 0 0 18 * * * | 分析对话质量 |
| 每日进化早报 | 0 0 8 * * * | 推送进化摘要 |
| 每日热榜推送 | 0 8 * * * | 推送热榜到飞书 |

---

## 📰 实用Skill速查

| Skill | 用途 | 命令 |
|:---|:---|:---|
| linfeng-novel | 番茄签约规范 | 读取 skills/linfeng-novel/SKILL.md |
| daily-hot-push | 每日热榜 | bash skills/daily-hot-push/push.sh |
| brave-search | 搜索工具 | web_search() |
| ai-evolution-engine-v2 | 自我进化 | bash skills/ai-evolution-engine-v2/scripts/evolve.sh |
