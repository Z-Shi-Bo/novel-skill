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
4. `Hook` 与 `Payoff` 都要有值；暂未确定时写 `TBD`，不要留空。
5. `End State` 必须说明本章结束后发生了什么变化。

## 常见错误

- 只有情绪描述，没有事件锚点
- `Progress Beats` 退化成一句话摘要
- `Hook` 与 `Payoff` 混成一条
