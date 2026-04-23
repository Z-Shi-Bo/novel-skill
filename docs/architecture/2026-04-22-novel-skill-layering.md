# novel / novel-framework / novel-ainovel-bridge 分层说明

日期：2026-04-22

## 目标

把小说相关能力拆成三层：

1. **全功能创作层**
2. **纯框架规划层**
3. **项目适配层**

避免出现：

- 一个 skill 同时承担所有职责而越来越重
- 通用 skill 被某个具体项目绑死
- 用户只想做框架时却误触正文生成

## 分层结果

### 1. `skills/novel`

定位：**通用长篇小说全功能 skill**。

负责：

- 项目初始化 `init`
- 立项定盘 `brief`
- 世界观与设定 `bible`
- 角色与关系 `characters`
- 卷纲 / 章纲 / chapter contract `outline`
- 状态维护 `state`
- 审稿 / 诊断 `review` / `diagnose`
- 样稿、tone reference、sample prose、章节草稿 `write`
- 改写 / 重写 / 扩写 `revise`
- 通用上下文包导出 `export`

不负责：

- AI-Novel 专属 feed 结构
- 某个具体项目的字段映射
- AI-Novel accepted 结果回流规则

一句话：

> `novel` 既能搭框架，也能写内容。

### 2. `skills/novel-framework`

定位：**通用长篇小说纯框架 skill**。

负责：

- 整体背景
- 世界观与设定铁律
- 人物角色与性格
- 势力、关系、钩子、故事情节骨架
- 卷纲 / 章纲 / chapter contract / chapter context
- 当前状态卡、伏笔池、时间线、资源账本
- 框架级诊断与研究

不负责：

- 样稿
- 对话试写
- 章节草稿
- 正文改写
- 正式正文

一句话：

> `novel-framework` 只做框架，不碰正文。

### 3. `skills/novel-ainovel-bridge`

定位：**AI-Novel 专属桥接层**。

负责：

- 把 `novel` 或 `novel-framework` 的控制面导出成 `ainovel_feed`
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

一句话：

> `bridge` 只接线，不创作。

## 推荐使用方式

### 想直接做小说、还能写内容

使用 `novel`：

- `$novel init`
- `$novel brief`
- `$novel bible`
- `$novel characters`
- `$novel outline`
- `$novel write`

### 只想做小说框架

使用 `novel-framework`：

- `$novel-framework init`
- `$novel-framework brief`
- `$novel-framework bible`
- `$novel-framework characters`
- `$novel-framework outline`

### 对接 AI-Novel

使用 `novel-ainovel-bridge`：

- `export`
- `sync`
- `resume`

## 这样拆分的好处

1. `novel` 保住全功能，不用被“阉割”
2. `novel-framework` 提供纯框架入口，避免误出正文
3. AI-Novel 适配逻辑集中，不污染通用 skill
4. 以后接别的项目时，只需新增新的 bridge skill
5. 职责边界清楚，维护成本更低

## 设计原则

一句话：

> `novel` 管创作全栈，`novel-framework` 管框架门面，`bridge` 管项目接线。
