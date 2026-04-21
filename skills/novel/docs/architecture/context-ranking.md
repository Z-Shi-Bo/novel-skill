# Context Ranking

## 目标

把上下文构建从“简单拼装”升级为“评分 + 解释”。

## 当前评分维度

- task 权重
- genre 权重
- chapter proximity
- hook / timeline continuity signal
- index artifact 加权

## 目标输出

```json
{
  "selected_items": [],
  "rejected_items": [],
  "scores": {},
  "reasoning_summary": ""
}
```

## 设计原则

1. 先规则排序，再考虑更复杂模型。
2. review 和 write 必须得到不同结果。
3. 结果必须能解释“为什么选它”。
