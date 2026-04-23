# novel

长篇小说**全功能** skill。

## 定位

这不是“一次性写一章”的 prompt，而是一个**文件化、可续写、可审查、可维护**的小说工作台。

当前版本的定位是：

- **框架 + 内容双栈**：既能做背景、设定、人物、纲要，也能写样章、草稿、正文
- **项目无关**：不内建任何特定外部项目的 feed 结构
- **桥接分离**：对接 AI-Novel 之类项目时，交给 bridge skill

它采用：

- 一书一目录
- 先立项再写
- 强闭环维护
- 按需联网考据
- 模板驱动落盘

## 适合什么场景

- 想从零开一本书，并长期维护
- 想同时做设定、大纲、人物、正文、改稿
- 想要一套可续写、可审查、可同步状态的创作控制面
- 有时直接用 skill 写正文，不依赖外部写作项目

## 不适合什么场景

- 只想做世界观 / 人设 / 大纲，不要正文  
  → 用 `novel-framework`
- 已经明确是 AI-Novel 项目交接 / accepted 回流  
  → 用 `novel-ainovel-bridge`
- 只想随口试一小段，不维护项目文件  
  → 讨论模式更合适

## 运行方式

本 skill 现在是 **prompt-native / template-native**：

- **不依赖 Python**
- **不依赖额外安装脚本**
- **不要求单独 CLI runtime**

使用时，直接通过 skill 自身说明、`templates/` 模板、`references/` 参考文档，以及宿主 CLI 的文件系统能力完成：

- 初始化项目目录
- 生成 brief / bible / characters / outline
- 写草稿与正式稿
- 生成摘要 / 审查 / 诊断
- 更新状态卡 / 伏笔池 / 时间线 / 资源账本
- 按需导出通用上下文包

## 安装

```powershell
npx skills add shibo1998/shibo-skills --skill novel
```

或：

```powershell
npx skills add https://github.com/shibo1998/shibo-skills --skill novel
```

## 在仓库中的位置

```text
skills/novel/
```

## skill 内容

```text
skills/novel/
├── .gitignore
├── SKILL.md
├── README.md
├── index.json
├── references/
├── templates/
└── docs/
```

## 项目结构

```text
projects/{novel-slug}/
├── project_manifest.yaml
├── 01_brief/
├── 02_bible/
├── 03_outline/
├── 04_manuscript/
├── 05_state/
├── 06_reports/
└── 07_exports/
```

## 你会得到什么

- 一套标准化小说项目目录
- 稳定的 brief / bible / characters / outline / manuscript / state / report 文件
- 可直接续写、审稿、改稿、诊断的长期创作面板
- 与 `novel-framework` / `novel-ainovel-bridge` 可组合协同的控制面

## 组合使用建议

- 想用一个 skill 从框架一路写到内容：用 `novel`
- 只想生成整体背景、大纲、人物角色、钩子、性格、故事情节框架：用 `novel-framework`
- 想把控制面喂给 AI-Novel 或同步 AI-Novel accepted 结果：用 `novel-ainovel-bridge`

## 最小使用流程

```text
/novel init
→ /novel brief
→ /novel bible
→ /novel characters
→ /novel outline
→ /novel write
→ /novel review
```

如果用户明确只要框架，不要继续写正文，就不要硬留在 `novel`，直接切到 `novel-framework`。

## 推荐入口

- `/novel init`
- `/novel brief`
- `/novel bible`
- `/novel characters`
- `/novel outline`
- `/novel write`
- `/novel revise`
- `/novel review`
- `/novel state`
- `/novel diagnose`
- `/novel research`
- `/novel export`
- `/novel resume`

## 说明

如果你只想要框架而不想输出任何正文，不要强行阉割 `novel`；直接使用独立的 `novel-framework`。  
如果你看到某个特定项目名（例如 AI-Novel）或专属 feed 结构，那属于桥接职责，交给 `novel-ainovel-bridge`。
