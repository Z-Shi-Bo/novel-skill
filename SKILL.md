---
name: novel
description: Create, plan, write, review, maintain, and resume long-form fiction projects with a file-based one-book-one-folder workflow. Use this whenever the user wants to start a novel, build story bible and outlines, write or revise chapters, maintain current story state, track hooks and continuity, diagnose long-form consistency, or resume a fiction project across sessions. Also use it for reality-grounded fiction that needs on-demand research and fact verification. Trigger aggressively for requests like “开一本新书”, “写第12章”, “续写”, “审稿”, “同步状态”, “做卷纲/章纲”, “恢复上次创作现场”, or explicit slash usage such as /novel.
version: 2.0.1
user-invocable: true
argument-hint: "[init|brief|bible|characters|outline|write|revise|review|state|diagnose|research|export|resume] [项目或需求]"
---

# novel wrapper

本仓库根目录是本地 CLI 发现用的包装层。

**真正的 skill 根目录是：**

```text
skills/novel/
```

继续前，先读取并遵循：

```text
skills/novel/SKILL.md
```

重要规则：

- 把 `skills/novel/` 当作真正的 skill root
- 后续所有相对路径都相对于 `skills/novel/` 解析
- scripts / references / templates / docs 都从 `skills/novel/` 下读取

例如：

- `skills/novel/scripts/...`
- `skills/novel/references/...`
- `skills/novel/templates/...`

除这层转发外，不要把仓库根目录当作 canonical skill source。
