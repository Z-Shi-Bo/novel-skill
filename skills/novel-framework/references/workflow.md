# Workflow

默认主链：

```text
init
→ brief
→ bible
→ characters
→ outline
→ state
→ diagnose
→ export
→ next step
```

## 阶段目标

| 阶段 | 目标 | 主要文件 |
|---|---|---|
| init | 建立项目壳子 | `project_manifest.yaml` |
| brief | 锁定题材、卖点、读者、风格 | `01_brief/project_brief.md` |
| bible | 固定世界规则与叙事口径 | `02_bible/story_bible.md` |
| characters | 固化人物与关系 | `02_bible/character_cards.md`, `02_bible/relationship_matrix.md` |
| outline | 先卷纲后章纲 | `03_outline/*` |
| state | 维护当前状态、伏笔、时间线 | `05_state/*` |
| diagnose | 做框架级或项目级诊断 | `06_reports/diagnostics/` |
| export | 导出通用上下文包 / chapter context | `07_exports/` |

## 默认规则

1. 未初始化项目时，不直接生成任何正文。
2. 本 skill 不生成 prose。
3. 未有章纲时，不生成 chapter context。
4. 框架诊断不过时，不建议切换到正文创作。

## 切换规则

- 需要正文 → 切换到 `novel`
- 需要 AI-Novel 对接 → 切换到 `novel-ainovel-bridge`
