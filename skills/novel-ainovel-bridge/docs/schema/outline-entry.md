# Outline Entry Mapping

适用链路：

- source：`03_outline/chapter_outlines/chNNN.md`
- target：`07_exports/ainovel_feed/outline.json`

## source 必备元信息

- `Chapter No`
- `Volume`
- `Working Title`
- `Core Event`

## target 章节字段

- `chapter`
- `title`
- `goal`
- `conflict`
- `coreEvent`
- `hook`
- `payoff`
- `endState`
- `scenes`

## 映射规则

1. `Working Title` → `title`
2. `Goal` → `goal`
3. `Conflict` → `conflict`
4. `Core Event` → `coreEvent`
5. `Hook / Payoff` → `hook` / `payoff`
6. `End State` → `endState`
7. `Progress Beats` 拆成 `scenes`
