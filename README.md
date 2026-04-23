# shibo-skills

自用 skill 仓库，按 `skills/<name>/` 组织，只保留 skill 分发与说明所需文件。

## 当前 skills

- `skills/novel` — 通用长篇小说**全功能** skill（框架 + 内容）
- `skills/novel-framework` — 通用长篇小说**纯框架** skill
- `skills/novel-ainovel-bridge` — `novel` / `novel-framework` 到 AI-Novel 的项目适配层

## 安装

本仓库按 **skills.sh / `npx skills add`** 的多 skill 仓库格式组织。

### 交互式安装（推荐）

```powershell
npx skills add shibo1998/shibo-skills --list
npx skills add shibo1998/shibo-skills
```

### 直接安装指定 skill

#### 全功能小说 skill

```powershell
npx skills add shibo1998/shibo-skills --skill novel
```

#### 纯框架 skill

```powershell
npx skills add shibo1998/shibo-skills --skill novel-framework
```

#### AI-Novel bridge

```powershell
npx skills add shibo1998/shibo-skills --skill novel-ainovel-bridge
```

### 也可用完整 GitHub URL

```powershell
npx skills add https://github.com/shibo1998/shibo-skills --skill novel
```

## 仓库结构

```text
skills/
├── novel/
│   ├── .gitignore
│   ├── SKILL.md
│   ├── README.md
│   ├── index.json
│   ├── docs/
│   ├── references/
│   └── templates/
├── novel-framework/
│   ├── .gitignore
│   ├── SKILL.md
│   ├── README.md
│   ├── index.json
│   ├── docs/
│   ├── references/
│   └── templates/
└── novel-ainovel-bridge/
    ├── .gitignore
    ├── SKILL.md
    ├── README.md
    ├── index.json
    ├── docs/
    ├── references/
    └── templates/
```

## 分层约定

- `novel`：负责立项、设定、角色、纲要、状态、伏笔、样稿、正文、改写
- `novel-framework`：负责小说整体背景、世界观、角色、钩子、故事骨架、状态与伏笔，不写正文
- `novel-ainovel-bridge`：负责 AI-Novel 专属 feed 导出与 accepted 结果回流
- 运行态目录如 `.omc/`、`projects/` 不进 git
- `index.json` 只列实际分发文件

## 推荐使用姿势

### 1. 只做框架

```powershell
npx skills add shibo1998/shibo-skills --skill novel-framework
```

适合：
- 只要背景 / 世界观 / 人设 / 纲要
- 不要正文
- 想先把控制面搭稳

### 2. 直接做小说（框架 + 内容）

```powershell
npx skills add shibo1998/shibo-skills --skill novel
```

适合：
- 想从立项一路写到章节内容
- 需要样章、草稿、改写、续写
- 不依赖外部正文项目

### 3. 框架 + AI-Novel 联动

```powershell
npx skills add shibo1998/shibo-skills --skill novel-framework
npx skills add shibo1998/shibo-skills --skill novel-ainovel-bridge
```

推荐流程：

1. 用 `novel-framework` 生成背景、角色、卷纲、章纲、状态卡
2. 用 `novel-ainovel-bridge` 导出 `ainovel_feed`
3. 在 AI-Novel 项目里跑正文 / 审稿 / 润色
4. 用 `novel-ainovel-bridge` 同步 accepted 结果回控制面

### 4. 全功能创作 + AI-Novel 联动

```powershell
npx skills add shibo1998/shibo-skills --skill novel
npx skills add shibo1998/shibo-skills --skill novel-ainovel-bridge
```

适合：
- 有时直接用 skill 写内容
- 有时把控制面喂给 AI-Novel
- 想保留更高创作自由度

## 本地验证声明

这个仓库的定位是：**仓库里只放可安装、可分发、可直接使用的 skill 资产**。

因此：

- `/skills/**`：属于分发内容，保留在仓库中
- `/tests/**`：只作为本地测试 / 回归 / 验证资产使用，不纳入仓库分发内容
- `/tools/**`：只作为本地辅助工具使用，不纳入仓库分发内容
- 任何运行态目录（如 `.omc/`、`projects/`）都不上传

换句话说：

> **仓库负责放“能用的 skill”，测试回归和验证链只在本地跑。**
