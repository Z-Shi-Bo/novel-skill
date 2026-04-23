# novel-ainovel-bridge

`novel` / `novel-framework` 通用控制面项目的 **AI-Novel 适配层**。

## 定位

这个 skill 不是拿来直接做小说创作的，也不是拿来从零生成大纲的，而是：

- 把 `skills/novel` 或 `skills/novel-framework` 产出的控制面导出成 AI-Novel 可消费的 feed / 参数包
- 把 AI-Novel 已 accepted 的结果回流到通用小说项目控制面

一句话说清：

> `novel-ainovel-bridge` 是“桥”，不是“起盘器”。
> 它负责把已有控制面打包成 AI-Novel 能吃的结构化输入，再把 accepted / final 结果同步回来。

也就是说：

- `novel` 负责：设定 / 角色 / 大纲 / 状态 / 伏笔 / 样稿参考 / 正文创作
- `novel-framework` 负责：纯框架（背景 / 大纲 / 人设 / 钩子 / 情节骨架）
- `novel-ainovel-bridge` 负责：AI-Novel 专属 packaging / sync
- `AI-Novel` 项目负责：正文 / 细节 / 审稿 / 润色流水线

## 安装

```powershell
npx skills add shibo1998/shibo-skills --skill novel-ainovel-bridge
```

或：

```powershell
npx skills add https://github.com/shibo1998/shibo-skills --skill novel-ainovel-bridge
```

## 典型使用场景

- “把这本书喂给 AI-Novel”
- “导出 ainovel_feed”
- “把 accepted 章节结果同步回控制面”
- “桥接 novel skill 和 AI-Novel 项目”

## 它能不能生成大纲，然后输出给 AI-Novel？

可以分成两半看：

### 1. 从零生成大纲

**这不是 bridge 的主职责。**

- 如果你要从零做背景 / 人设 / 卷纲 / 章纲 / chapter context，请先用 `novel-framework`
- 如果你既要框架又要正文创作，请先用 `novel`

### 2. 输出给 AI-Novel 使用的参数

**这正是 bridge 的主职责之一。**

它可以把已有控制面导出成 AI-Novel 可消费的结构化 handoff，包括：

- `manifest.yaml`
- `premise.md`
- `characters.json`
- `world_rules.json`
- `outline.json`
- `foreshadows.json`
- `chapter_context/chNNN.yaml`
- `overrides/writer.override.md`
- `overrides/reviewer.override.md`

所以更准确地说：

> `novel-ainovel-bridge` 不负责从零起盘生成大纲，
> 但它负责把**已有大纲与控制面**转成 AI-Novel 能直接使用的参数包。

## 不适合什么场景

- 从零开始发明世界观、人设、主线、卷纲、章纲
- 直接写正文、改正文、润色正文
- 没有通用控制面项目就想硬导 feed
- 没有上游框架，却希望它一边起盘一边导出 AI-Novel 参数

## 最小使用流程

### export

1. 先用 `novel` 或 `novel-framework` 产出控制面（brief / bible / characters / outline / state）
2. 再执行 bridge 导出 feed

### sync

1. 确认 AI-Novel 侧已经得到 accepted / final 结果
2. 准备 accepted payload（至少包含 `chapter`、`accepted=true`、`summary`、`state_updates`、`hook_updates`；推荐补 `payload_id`、`chapter_revision`、`accepted_at`）
3. 再执行 bridge 回流控制面

默认把同一 `payload_id` 当作同一同步单元；重复执行应按 upsert 处理，不应重复追加。
如果一次同步多章，默认按章节号升序处理。
章节摘要目标文件统一使用 `06_reports/chapter_summaries/chNNN_summary.md`。

### batch sync

`sync` 除了吃单个 accepted payload，也可以直接吃：

- 一个 accepted payload 目录
- 一个 batch manifest

适合场景：

- 一次把多个已 accepted 章节回流
- 同章有 replay / retry，需要按 `payload_id` 去重
- 想明确指定本次回流顺序

## 你会得到什么

- 一套稳定的 `ainovel_feed` 导出物
- accepted payload / batch manifest 的回流合同
- 通用控制面与 AI-Novel 之间清晰、可追踪、可重复执行的交接层

## AI-Novel 可消费参数说明

bridge 导出的核心不是 prose，而是 handoff 参数：

- `premise.md`：项目总 premise，给 AI-Novel 抓主线和基调
- `characters.json`：角色卡结构化数据
- `world_rules.json`：世界规则与一致性边界
- `outline.json`：卷 / 弧 / 章目标、conflict、hook、payoff、endState、scenes
- `foreshadows.json`：伏笔账本
- `chapter_context/chNNN.yaml`：当前章必须承接的上下文
- `overrides/*`：writer / reviewer 的项目级约束

如果你问的是“它能不能输出 AI-Novel 项目使用的参数”——答案是：**能，而且这就是它最核心的价值。**

## 推荐组合

- `novel + novel-ainovel-bridge`：适合既要直接创作又要接 AI-Novel
- `novel-framework + novel-ainovel-bridge`：适合“skill 只做框架，项目负责正文”

推荐理解方式：

- `novel` / `novel-framework`：负责“想清楚”
- `novel-ainovel-bridge`：负责“交出去”
- `AI-Novel`：负责“跑正文流水线”

桥接层不负责写正文，它只负责：
- 把控制面转成 AI-Novel 可消费格式
- 把 AI-Novel accepted 结果回流到控制面
- 拒绝把 draft / polish 中间态误当成 canon

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
- `docs/schema/accepted-sync-payload.md`：accepted 回流合同
- `docs/schema/accepted-sync-batch.md`：多章节 / 批量回流合同
- `docs/schema/chapter-context.md` / `character-card.md` / `outline-entry.md`：归一化字段说明
- `references/workflow.md`：export / sync 流程
- `templates/*`：feed 模板
