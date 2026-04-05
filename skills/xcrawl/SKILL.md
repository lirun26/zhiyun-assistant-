# XCrawl Skill

网页抓取工具，把网站转成结构化 JSON / Markdown。

## 命令

### 抓取网页
```bash
npx @xcrawl/cli scrape <URL> --format json
npx @xcrawl/cli scrape <URL> --format markdown
```

### 搜索
```bash
npx @xcrawl/cli search "<query>" --format json
```

### 站点地图
```bash
npx @xcrawl/cli map <URL>
```

### 账号状态
```bash
npx @xcrawl/cli status
```

## 使用场景
- 抓取网页正文（代替 web_fetch）
- 获取结构化数据（JSON 格式）
- 搜索关键词获取 SERP 数据
- 抓取被反爬保护的网站

## 注意事项
- 默认格式：markdown（最节省 tokens）
- JSON 格式：适合程序处理
- 免费额度：1000 credits/月
