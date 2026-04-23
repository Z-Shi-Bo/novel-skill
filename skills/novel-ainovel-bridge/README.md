# novel-ainovel-bridge

`novel` 通用控制面 skill 的 **AI-Novel 适配层**。

## 定位

这个 skill 不是拿来直接做小说创作的，而是：

- 把 `skills/novel` 产出的控制面导出成 AI-Novel 可消费的 feed
- 把 AI-Novel 已 accepted 的结果回流到通用小说项目控制面

也就是说：

- `novel` 负责：设定 / 角色 / 大纲 / 状态 / 伏笔 / 样稿参考 / 正文创作
- `novel-framework` 负责：纯框架（背景 / 大纲 / 人设 / 钩子 / 情节骨架）
- `novel-ainovel-bridge` 负责：AI-Novel 专属 packaging / sync
- `AI-Novel` 项目负责：正文 / 细节 / 审稿 / 润色流水线

## 安装

```powershell
$env:SKILL_BASE_URL='https://raw.githubusercontent.com/shibo1998/shibo-skills/main/'
npx skill skills/novel-ainovel-bridge
```

## 典型使用场景

- “把这本书喂给 AI-Novel”
- “导出 ainovel_feed”
- “把 accepted 章节结果同步回控制面”
- “桥接 novel skill 和 AI-Novel 项目”

## 主要产物

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

## 文件说明

- `SKILL.md`：bridge 行为规则
- `docs/schema/ainovel-feed.md`：feed 结构说明
- `references/workflow.md`：export / sync 流程
- `templates/*`：feed 模板
