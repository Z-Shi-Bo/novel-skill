# Accepted Sync Batch Schema

适用 skill：`novel-ainovel-bridge`

## 目标

用于一次回流多章 accepted 结果，或者显式指定本次 `sync` 应处理哪些 payload、按什么顺序处理。

## 适用场景

- accepted payload 放在同一目录下，想整批回流
- 同一章节存在 replay / retry，需要显式去重
- 想把多章回流顺序固定下来

## 推荐文件

- `07_exports/ainovel_results/accepted/batch_sync.yaml`

## 最小结构

```yaml
mode: accepted_batch
items:
  - chapter: 1
    payload: 07_exports/ainovel_results/accepted/ch001_sync.yaml
  - chapter: 2
    payload: 07_exports/ainovel_results/accepted/ch002_sync.yaml
```

## 推荐字段

- `mode`：固定为 `accepted_batch`
- `items[].chapter`
- `items[].payload`
- `items[].payload_id`
- `items[].chapter_revision`
- `items[].accepted_at`
- `items[].note`

## 处理规则

1. `items` 不能为空。
2. 默认按 `items[].chapter` 升序处理；如果 manifest 顺序与章节顺序冲突，以章节顺序优先。
3. 同一同步单元优先用 `payload_id` 去重；没有 `payload_id` 时，用 `chapter + accepted_at + payload` 回退识别。
4. 任一条目指向的 payload 不是 accepted / final 时，应中止并报冲突。
5. 同章出现更高 `chapter_revision` 或更晚 `accepted_at` 时，后者 supersede 前者。
