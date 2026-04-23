# shibo-skills

自用 skill 仓库，按 `skills/<name>/` 组织，只保留 skill 分发与说明所需文件。

## 当前 skills

- `skills/novel` — 通用长篇小说**全功能** skill（框架 + 内容）
- `skills/novel-framework` — 通用长篇小说**纯框架** skill
- `skills/novel-ainovel-bridge` — `novel` / `novel-framework` 到 AI-Novel 的项目适配层

## 安装

### 全功能小说 skill

```powershell
$env:SKILL_BASE_URL='https://raw.githubusercontent.com/shibo1998/shibo-skills/main/'
npx skill skills/novel
```

### 纯框架 skill

```powershell
$env:SKILL_BASE_URL='https://raw.githubusercontent.com/shibo1998/shibo-skills/main/'
npx skill skills/novel-framework
```

### AI-Novel bridge

```powershell
$env:SKILL_BASE_URL='https://raw.githubusercontent.com/shibo1998/shibo-skills/main/'
npx skill skills/novel-ainovel-bridge
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

## 本地验证声明

这个仓库的定位是：**仓库里只放可安装、可分发、可直接使用的 skill 资产**。

因此：

- `/skills/**`：属于分发内容，保留在仓库中
- `/tests/**`：只作为本地测试 / 回归 / 验证资产使用，不纳入仓库分发内容
- `/tools/**`：只作为本地辅助工具使用，不纳入仓库分发内容
- 任何运行态目录（如 `.omc/`、`projects/`）都不上传

换句话说：

> **仓库负责放“能用的 skill”，测试回归和验证链只在本地跑。**
