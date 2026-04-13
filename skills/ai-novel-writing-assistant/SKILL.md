# AI-Novel-Writing-Assistant Skill

## 功能概述
封装调用 AI-Novel-Writing-Assistant 项目的能力，支持从灵感生成整本小说、章节生成、角色管理、世界观构建等。

## 项目信息
- **地址**: `/home/admin/.openclaw/workspace/AI-Novel-Writing-Assistant`
- **前端**: http://localhost:5173
- **后端**: http://localhost:3000
- **状态**: ✅ 已安装并运行

## API 基础
- Base URL: `http://localhost:3000/api`
- 返回格式: `{ success: boolean, data?: T, error?: string }`
- 流式输出: `text/event-stream` (SSE)

## 快速使用流程

### 1. 创建小说
```bash
curl -s -X POST http://localhost:3000/api/novels \
  -H "Content-Type: application/json" \
  -d '{"title": "小说标题", "idea": "核心创意"}' | jq .data.id
```

### 2. 绑定世界观（可选）
```bash
# 先创建世界观
curl -s -X POST http://localhost:3000/api/worlds \
  -H "Content-Type: application/json" \
  -d '{"name": "世界观名", "description": "描述", "novelId": "小说ID"}'
```

### 3. 添加角色（必须）
```bash
# 先创建基础角色库
curl -s -X POST http://localhost:3000/api/base-characters \
  -H "Content-Type: application/json" \
  -d '{"name": "叶辰", "role": "protagonist", "personality": "沉稳果断", "background": "前世仙帝", "category": "fantasy"}'

# 绑定到小说
curl -s -X POST "http://localhost:3000/api/novels/{novelId}/characters" \
  -H "Content-Type: application/json" \
  -d '{"name": "叶辰", "role": "protagonist", "castRole": "protagonist", "baseCharacterId": "角色ID", "personality": "沉稳果断", "background": "背景"}'
```

### 4. 创建章节
```bash
curl -s -X POST "http://localhost:3000/api/novels/{novelId}/chapters" \
  -H "Content-Type: application/json" \
  -d '{"title": "第1章标题", "order": 1}' | jq .data.id
```

### 5. 生成章节内容（流式）
```bash
curl -s -N -X POST "http://localhost:3000/api/novels/{novelId}/chapters/{chapterId}/generate" \
  -H "Content-Type: application/json" \
  -d '{"provider": "siliconflow", "model": "Qwen/Qwen2.5-7B-Instruct"}'
```

### 6. 获取章节内容
```bash
curl -s "http://localhost:3000/api/novels/{novelId}/chapters" | jq '.data[0].content'
```

## Creative Hub 对话（需先绑定novelId到线程）
```bash
# 创建线程并绑定小说
curl -s -X POST "http://localhost:3000/api/creative-hub/threads" \
  -H "Content-Type: application/json" \
  -d '{"title": "创作对话", "resourceBindings": {"novelId": "小说ID"}}'

# 发送对话（SSE流式）
curl -s -N -X POST "http://localhost:3000/api/creative-hub/threads/{threadId}/runs/stream" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"type": "human", "content": "你的问题"}], "provider": "siliconflow", "model": "Qwen/Qwen2.5-7B-Instruct"}'
```

## 其他API

| 功能 | API |
|:---|:---|
| 小说列表 | `GET /api/novels` |
| 小说详情 | `GET /api/novels/{id}` |
| 题材类型 | `GET /api/genres` |
| 世界观列表 | `GET /api/worlds` |
| 基础角色 | `GET /api/base-characters` |
| 章节列表 | `GET /api/novels/{id}/chapters` |
| 写法引擎 | `GET /api/style-engine/styles` |

## 模型配置
- **推荐**: SiliconFlow (`***MASKED***`)
- **配置位置**: `/home/admin/.openclaw/workspace/AI-Novel-Writing-Assistant/server/.env`

## 注意事项
- 后端启动: `cd AI-Novel-Writing-Assistant && pnpm dev`
- 必须先添加角色才能生成章节
- RAG功能默认关闭（如需启用配置Qdrant）
- Creative Hub 需要在创建线程时绑定novelId
