# shibo-skills

自用 skill 仓库，按 `skills/<name>/` 组织，只保留 skill 分发与说明所需文件。

## 当前 skills

- `skills/novel` — 通用长篇小说控制面 skill
- `skills/novel-ainovel-bridge` — `novel` 到 AI-Novel 的项目适配层

## 安装

### 通用小说 skill

```powershell
$env:SKILL_BASE_URL='https://raw.githubusercontent.com/shibo1998/shibo-skills/main/'
npx skill skills/novel
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

- `novel`：负责立项、设定、角色、纲要、状态、伏笔、样稿参考
- `novel-ainovel-bridge`：负责 AI-Novel 专属 feed 导出与 accepted 结果回流
- 运行态目录如 `.omc/`、`projects/` 不进 git
- `index.json` 只列实际分发文件
- 本地测试 / 回归 / 安全验证资产不上传
