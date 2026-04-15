# Errors Log

Non-obvious command failures, tool/API issues, exceptions, and recurring operational problems.

**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted

## When to log here

Use this file when the failure is worth remembering, not for every routine error.

Good candidates:
- required real debugging or investigation
- likely to recur
- revealed an environment or tooling gotcha
- should influence future troubleshooting steps

## Entry template

```markdown
## [ERR-YYYYMMDD-XXX] error-name

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: resolved
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description of what failed

### Error
```
Raw error message or representative output
```

### Context
What command, tool, API, or workflow was involved

### Suggested Fix
What to try next time or how to prevent recurrence

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20260313-001

---
```

---

## [ERR-20260414-001] ai-evolution-engine脚本路径错误

**Logged**: 2026-04-14T15:14:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: infra

### Summary
ai-evolution-engine-v2的assess.mjs脚本中引用了错误的相对路径`../../skills`

### Error
```
ENOENT: no such file or directory, scandir '../../skills'
```

### Context
运行 `node skills/ai-evolution-engine-v2/scripts/assess.mjs`

### Suggested Fix
修复脚本中的路径引用，从`../../skills`改为正确的skills目录路径

### Metadata
- Reproducible: yes
- Related Files: skills/ai-evolution-engine-v2/scripts/assess.mjs

---

## [NOVEL-ERR-20260415-001] 小说角色认知逻辑错误

**Logged**: 2026-04-15T19:31:00+08:00
**Priority**: high
**Status**: resolved
**Area**: docs

### Summary
第3章结尾赵万隆说"输给一个摆摊的年轻人"，但赵万隆根本不知道顾玄青的存在，逻辑矛盾

### Error
```
原文："我花了那么多钱，请了那么多高人，怎么可能输给一个摆摊的年轻人……"
修正："我花了那么多钱，请了玄机子这样的高人，怎么可能输给周明山那边的人……"
```

### Context
小说创作第3章《噬魂阵》

### Suggested Fix
1. 写反派对白前，先确认该角色是否知道主角的存在
2. 反派知道的信息只能：通过观察/调查/猜测得到的，不能凭空捏造
3. 每章写完后检查：所有角色的认知是否与其身份/经历匹配

### Metadata
- Reproducible: yes
- Related Files: novels/天机风水商途/第03章_噬魂阵.md
- Prevention: 创作checklist增加"角色认知逻辑检查"

---
