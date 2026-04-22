# shibo-skills

自用 skill 仓库，按 `skills/<name>/` 组织，只保留 skill 分发与说明所需文件。

## 当前 skills

- `skills/novel` — 长篇小说项目型 skill

## 安装

当前 `novel` skill 可通过 `npx skill` 安装：

```powershell
$env:SKILL_BASE_URL='https://raw.githubusercontent.com/shibo1998/shibo-skills/main/'
npx skill skills/novel
```

## 仓库结构

```text
skills/
└── novel/
    ├── .gitignore
    ├── SKILL.md
    ├── README.md
    ├── index.json
    ├── docs/
    ├── references/
    └── templates/
```

## 约定

- 每个 skill 独立放在 `skills/<name>/`
- 仓库只提交 skill 相关文件
- 本地测试 / 回归 / 安全验证资产不上传
- 运行态目录如 `.omc/`、`projects/` 不进 git
- `index.json` 只列实际分发文件
