# novel / novel-ainovel-bridge 分层说明

日期：2026-04-22

## 目标

把原先混在一个 skill 里的“通用小说控制面能力”和“AI-Novel 项目适配能力”拆开，避免通用 skill 被某个具体项目绑死。

## 分层结果

### 1. `skills/novel`

定位：**通用长篇小说控制面 skill**。

负责：

- 项目初始化 `init`
- 立项定盘 `brief`
- 世界观与设定 `bible`
- 角色与关系 `characters`
- 卷纲 / 章纲 / chapter contract `outline`
- 状态维护 `state`
- 审稿 / 诊断 `review` / `diagnose`
- 样稿、tone reference、sample prose `write`
- 通用上下文包 / chapter context 导出 `export`

不负责：

- AI-Novel 专属 feed 结构
- 某个具体项目的字段映射
- AI-Novel accepted 结果回流规则

原则：

- 用户已有外部正文项目时，`novel` 默认只产控制面和样稿参考
- 正式正文 canon 不由 `novel` 默认接管

### 2. `skills/novel-ainovel-bridge`

定位：**AI-Novel 专属桥接层**。

负责：

- 把 `novel` 的控制面导出成 `ainovel_feed`
- 生成 AI-Novel 专属模板：
  - `manifest.yaml`
  - `premise.md`
  - `characters.json`
  - `world_rules.json`
  - `outline.json`
  - `foreshadows.json`
  - `chapter_context/chNNN.yaml`
  - `writer.override.md`
  - `reviewer.override.md`
- 规划 AI-Novel accepted 结果如何回流到通用控制面

不负责：

- 小说设定本体的创作
- 正文写作本身
- 代替 AI-Novel 的 writer / editor / polisher

## 推荐使用方式

### 通用创作阶段

使用 `novel`：

- `$novel init`
- `$novel brief`
- `$novel bible`
- `$novel characters`
- `$novel outline`
- `$novel state`

### 对接 AI-Novel 阶段

使用 `novel-ainovel-bridge`：

- 导出 feed
- 同步 accepted 结果
- 管理项目专属 override

## 这样拆分的好处

1. `novel` 继续保持通用，可接更多正文项目
2. AI-Novel 适配逻辑集中，不污染通用 skill
3. 以后接别的项目时，只需新增新的 bridge skill
4. 维护成本下降，职责边界更清楚

## 设计原则

一句话：

> `novel` 管小说本体，`bridge` 管项目接线。
