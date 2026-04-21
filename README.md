# Universal Novel Studio

通用长篇小说项目工作台型 skill 包。

它**不是只生成大纲**，也**不是只生成正文**。  
它覆盖的是整条小说主链：

- 新建小说项目
- 立项定盘
- 设定圣经
- 角色与关系
- 卷纲 / 章纲
- 正文写作
- 改写 / 重写 / 扩写 / 润色
- 审稿与诊断
- 状态同步
- 伏笔维护
- 恢复续写
- 按需联网考据

## 默认工作方式

默认采用：

- 一书一目录
- 先立项再写
- 强闭环维护
- 按需联网考据

也就是说，它默认不是“上来就写正文”，而是：

```text
项目初始化
→ brief
→ bible
→ characters
→ outline
→ write
→ review
→ sync
→ diagnose
→ next chapter
```

## 这个 skill 到底是做什么的？

### 如果你问：它是生成小说还是生成大纲？

正确答案是：**两者都做，但顺序上优先先把项目控制面搭起来。**

- 当项目还没建立好时，它先帮你做：定位、设定、卷纲、章纲。
- 当项目已经进入写作阶段时，它帮你做：正文、修稿、审稿、状态维护。

所以它更准确的定位是：

> **小说项目操作系统 / 小说工作台**

而不是“单一大纲生成器”或“单一正文生成器”。

## 目录

```text
universal-novel-studio/
├── SKILL.md
├── references/
├── templates/
├── scripts/
└── evals/
```

## 运行前要求

- Python 3.10+
- 可读写本地文件系统
- 如果要跑现实题材考据，允许联网搜索

## 安装方式

如果你只是本地使用，保持当前目录结构即可。  
如果你要把它作为 skill 包挪到别处，至少要完整保留：

- `SKILL.md`
- `references/`
- `templates/`
- `scripts/`
- `evals/`

不要只拷贝 `SKILL.md`，否则这个包会退化成没有执行层的半成品。

## 快速开始

### 1. 初始化一本新书

```powershell
python "scripts\init_project.py" `
  --workspace "C:\path\to\universal-novel-studio" `
  --templates "C:\path\to\universal-novel-studio\templates" `
  --title "你的书名" `
  --genre "都市悬疑" `
  --style "冷硬现实" `
  --audience "18-35"
```

### 2. 构建上下文包

```powershell
python "scripts\build_context.py" --project "...\projects\你的书slug" --task write --chapter 1
```

### 3. 同步章节状态

```powershell
python "scripts\update_state.py" --project "...\projects\你的书slug" --chapter 1 --volume 1
```

### 4. 跑诊断

```powershell
python "scripts\diagnose_project.py" --project "...\projects\你的书slug" --scope project
```

### 5. 生成 research note

```powershell
python "scripts\research_context.py" `
  --project "...\projects\你的书slug" `
  --topic "1993-hk-radio" `
  --question "1993年香港巡警常见通讯设备是什么？"
```

### 6. 生成章节摘要

```powershell
python "scripts\summarize_chapter.py" --project "...\projects\你的书slug" --chapter 1
```

## 命令面

推荐命令：

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

## CLI Shell（v2.0 方向）

当前已提供统一 CLI 入口雏形：

```powershell
python "cli\novel_cli.py" --help
python "cli\novel_cli.py" init --help
python "cli\novel_cli.py" diagnose --help
```

已收口的命令包括：

- `init`
- `review`
- `diagnose`
- `context`
- `sync`
- `research`

## 适合什么场景

适合：

- 想系统性写长篇小说
- 不想每次续写都重新解释设定
- 希望维护状态卡、伏笔池、摘要、审查报告
- 现实题材需要查资料
- 想把 summary / review / research 都做成可追踪索引

不适合：

- 只想随手写一小段、完全不建项目结构
- 完全不需要文件化管理

## 核心区别

和普通“小说 prompt”相比，这个包的核心差异是：

1. **有项目结构**
2. **有状态控制面**
3. **有强闭环维护**
4. **有审查和诊断**
5. **有 research note 落盘**

所以它不是只帮你“生成一段文字”，而是帮你**持续经营一部小说项目**。

## 推荐调用顺序

### 从零开始开一本书

```text
/novel init
→ /novel brief
→ /novel bible
→ /novel characters
→ /novel outline
→ /novel write
→ /novel review
→ /novel state
→ /novel diagnose
```

### 已有项目继续写

```text
/novel resume
→ /novel write
→ /novel review
→ /novel state
→ /novel diagnose
```

### 现实题材章节

```text
/novel research
→ /novel outline
→ /novel write
→ /novel review
```

## 示例与样板

已提供样板文档：

- `docs/examples/urban-mystery.md`
- `docs/examples/period-fiction.md`
- `docs/examples/fantasy.md`

建议先按最接近你题材的样板走一轮，再定制自己的项目。

## v1.2 新增

- `build_context.py` 接入 `research_index.md`
- `diagnose_project.py` 增加 Severity Summary
- `chapter_summary` / `review_report` 自动索引
- `research note` 自动写入统一索引

## v1.3 新增

- `build_context.py` 接入 `summary_index.md`、`review_index.md`、`research_index.md`
- `diagnose_project.py` 跑诊断前自动同步 summary / review 索引
- `summary_index.md` 与 `review_index.md` 正式纳入项目级控制面
- 诊断逻辑增强：草稿/正式稿链路、占位词、索引缺失、角色/关系空表等
- README 增补为更完整的实战工作流说明

## v1.4 新增

- `sync_indexes.py`：统一同步 summary / review 索引
- `write_review.py`：自动生成基础 review 报告
- `diagnose_project.py --json-out`：输出机器可读诊断
- `build_context.py`：增加题材化上下文优先级与风险标签
- 新增 `CHANGELOG.md`
