# Workflow

默认主链：

```text
init
→ brief
→ bible
→ characters
→ outline
→ write
→ review
→ finalize
→ sync
→ diagnose
→ next chapter
```

## 阶段目标

| 阶段 | 目标 | 主要文件 |
|---|---|---|
| init | 建立项目壳子 | `project_manifest.yaml` |
| brief | 锁定题材、卖点、读者、风格 | `01_brief/project_brief.md` |
| bible | 固定世界规则与叙事口径 | `02_bible/story_bible.md` |
| characters | 固化人物与关系 | `02_bible/character_cards.md`, `02_bible/relationship_matrix.md` |
| outline | 先卷纲后章纲 | `03_outline/*` |
| write | 生成章节草稿 | `04_manuscript/drafts/` |
| review | 做四层审查 | `06_reports/reviews/` |
| finalize | 写正式稿 | `04_manuscript/chapters/` |
| sync | 完成摘要与状态更新 | `05_state/*`, `06_reports/chapter_summaries/` |
| diagnose | 做章节级或项目级诊断 | `06_reports/diagnostics/` |

## 默认规则

1. 未初始化项目时，不直接写正文。
2. 未有章纲时，不默认写正式章节。
3. 写完草稿后，先 review，再定稿。
4. 定稿后必须执行 sync。
5. 章节未 `synced` 时，不视为完成。

## 外部项目说明

- `novel` 可以独立完成小说框架与正文创作。
- 如果用户有外部正文项目，也可以继续使用 `novel` 创作内容。
- 但任何**项目专属 feed / schema / import mapping** 不属于这里，交给 bridge skill。

## 讨论模式

下面这些默认只讨论，不落盘：

- 比题材
- 问方向是否成立
- 讨论主角设定是否有吸引力
- 讨论卷纲策略但不要求正式生成文件

只有用户明确要“创建 / 更新 / 写入 / 生成项目文件”时，再进入落盘模式。
