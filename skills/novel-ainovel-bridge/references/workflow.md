# Workflow

## export

```text
读取通用小说控制面
→ 检查必要文件是否齐全
→ 组装 ainovel_feed
→ 增量写入 07_exports/ainovel_feed/
→ 返回导出结果
```

## sync

```text
读取 AI-Novel accepted 结果
→ 如果输入是目录或 batch manifest，先展开条目
→ 按 chapter 升序 / payload_id 去重
→ 提取摘要 / 状态变化 / 伏笔推进
→ 回流 current_state / pending_hooks / summaries
→ 标注同步范围与遗留风险
```

## 默认规则

1. 缺少通用控制面文件时，不硬导出 feed。
2. 只回流 accepted / final 结果，不回流 draft。
3. 不直接生成正式正文。
4. 不替代 AI-Novel 项目的 writer / editor / polisher。
5. 同一 payload 重复执行时，按 upsert 处理，不重复追加。
6. batch manifest 只负责列条目与顺序，不替代单个 payload 合同。
