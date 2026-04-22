# Workflow

默认主链：

```text
init
→ brief
→ bible
→ characters
→ outline
→ chapter context
→ write / sample prose
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
| chapter context | 生成本章意图包 / 契约 / 语气约束 | `07_exports/context_packs/` |
| write | 生成章节草稿或样稿 | `04_manuscript/drafts/` |
| review | 做四层审查 | `06_reports/reviews/` |
| finalize | 写正式稿 | `04_manuscript/chapters/` |
| sync | 完成摘要与状态更新 | `05_state/*`, `06_reports/chapter_summaries/` |
| diagnose | 做章节级或项目级诊断 | `06_reports/diagnostics/` |

## 默认规则

1. 未初始化项目时，不直接写正文。
2. `init` 是脚手架动作：只建壳子，不做创意访谈，不自动进入后续阶段。
3. 未有章纲时，不默认写正式章节。
4. 如果用户已有外部写作项目，默认先输出控制面与样稿参考，不直接写正式章节。
5. 写完草稿后，先 review，再定稿。
6. 定稿后必须执行 sync。
7. 章节未 `synced` 时，不视为完成。

## 双模式

### 1. standalone 模式

- 本 skill 直接写草稿 / 正式稿
- 适合没有外部正文引擎的项目

### 2. external-engine 模式

- 本 skill 负责控制面、chapter context、样稿参考
- 外部项目负责正文、细节、审稿、润色
- accepted 结果再回流到本项目状态卡
- 项目专属 packaging 由对应 bridge skill 负责

只要用户明确提到外部项目 / engine / pipeline，默认进入 external-engine 模式。

## 讨论模式

下面这些默认只讨论，不落盘：

- 比题材
- 问方向是否成立
- 讨论主角设定是否有吸引力
- 讨论卷纲策略但不要求正式生成文件

只有用户明确要“创建 / 更新 / 写入 / 生成项目文件”时，再进入落盘模式。
