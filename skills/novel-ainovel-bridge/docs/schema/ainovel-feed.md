# AI-Novel Feed Schema

适用目录：`07_exports/ainovel_feed/`

## 目标

这个目录用于把本 skill 规划好的**控制面**喂给外部写作项目。

默认包含：

```text
07_exports/ainovel_feed/
├── manifest.yaml
├── premise.md
├── characters.json
├── world_rules.json
├── outline.json
├── foreshadows.json
├── chapter_context/
│   └── chNNN.yaml
└── overrides/
    ├── writer.override.md
    └── reviewer.override.md
```

## 字段职责

| 文件 | 用途 | 说明 |
|---|---|---|
| `manifest.yaml` | handoff 元信息 | 指明 feed 版本、项目 slug、当前章、目标字数区间、source of truth |
| `premise.md` | 总 premise | 融合 brief / bible / 关系 / 风格要求 |
| `characters.json` | 角色结构化卡片 | 供外部项目写入角色库 |
| `world_rules.json` | 世界规则边界 | 供外部项目做一致性控制 |
| `outline.json` | 卷弧章结构 | 供外部项目读取章目标与 hook |
| `foreshadows.json` | 伏笔账本 | 供外部项目承接 planted / hinted / resolved 状态 |
| `chapter_context/chNNN.yaml` | 本章意图包 | must_keep / must_avoid / emotion_target / hook_goal / continuity_notes |
| `overrides/writer.override.md` | 写作加严规则 | 项目级文风、禁用词、节奏要求 |
| `overrides/reviewer.override.md` | 审稿加严规则 | 外部项目 review 时的额外门槛 |

## 章节意图包最小字段

`chapter_context/chNNN.yaml` 至少应包含：

- `chapter`
- `title`
- `must_keep`
- `must_avoid`
- `emotion_target`
- `hook_goal`
- `continuity_notes`

推荐附加：

- `voice_notes`
- `required_beats`
- `forbidden_moves`
- `active_hooks`
- `state_focus`

## 同步原则

1. 先更新 control-plane 文件，再导出 handoff。
2. 外部项目 accepted 的正文，才能回流为 canon。
3. 样稿 / 试写 / tone reference 不能直接回流为正文 canon。
4. handoff 包优先增量更新，不整包重写。
