# Outline Entry Schema

适用文件：`03_outline/chapter_outlines/chNNN.md`

## 必备元信息

- `Chapter No`
- `Volume`
- `Working Title`
- `Core Event`

## 必备区块

- `Goal`
- `Conflict`
- `Progress Beats`
- `Hook / Payoff`
- `End State`

## 推荐区块

- `Canon Risks`

## 校验规则

1. `Chapter No` / `Volume` 应能解析为整数。
2. `Core Event` 应是一句能锚定本章主事件的短句。
3. `Progress Beats` 至少 3 条。
4. `Hook` 与 `Payoff` 都要有值；未知时写 `TBD`。
5. `End State` 必须落到状态变化，而不是抽象主题。

## 常见错误

- 章纲只有主题，没有事件
- `Progress Beats` 全是同义改写
- `Payoff` 留空，导致后续 export 无法组 contract
