# novel skill 拆分后续修改清单

日期：2026-04-22

## 当前已完成

- `novel` 回收为通用控制面 skill
- `novel-ainovel-bridge` 新建为 AI-Novel 专属桥接层
- 根 README 与各 skill README 已更新
- 分发索引已拆分
- smoke / guardrail 回归已通过

## 后续建议修改

### P1：bridge 的 export / sync 细化

1. 明确 AI-Novel 当前真实消费字段与文件名
2. 把 `ainovel_feed` 模板从占位模板升级成“字段级规范”
3. 明确 `sync` 时哪些 accepted 结果可回流：
   - summary
   - pending hooks
   - current state
   - timeline
   - relationship changes

### P1：通用 `export` 与 bridge `export` 的边界再收紧

1. `novel export` 目前仍是通用导出语义，建议后续限定为：
   - 通用上下文包
   - chapter context
   - summary bundle
2. AI-Novel feed 一律交给 `novel-ainovel-bridge export`

### P1：补 bridge 的回归测试

当前 harness 覆盖的是 `novel` 的：

- smoke init
- guardrail: 无章纲禁止写正文

建议补：

1. `bridge export` 成功导出 feed
2. `bridge export` 在缺少控制面文件时正确报错
3. `bridge sync` 仅 accepted 结果可回流
4. `bridge sync` 遇到 draft 时拒绝回流

### P2：补 bridge 的 fixture

建议新增：

- 一个完整 `novel` 控制面 fixture
- 一个 AI-Novel accepted fixture
- 一个 AI-Novel draft-only fixture

### P2：统一 chapter context 语义

目前 `chapter_context.yaml` 已存在于通用层与 bridge 层。
后续建议统一字段定义，避免两边未来漂移。

可固定为：

- chapter
- title
- must_keep
- must_avoid
- emotion_target
- hook_goal
- continuity_notes
- voice_notes
- required_beats
- forbidden_moves

### P2：补安装说明与组合用法示例

建议在 README 里新增一个最小示例：

1. `$novel init`
2. `$novel brief`
3. `$novel bible`
4. `$novel outline`
5. `$novel-ainovel-bridge export`
6. AI-Novel 跑正文
7. `$novel-ainovel-bridge sync`

### P3：命名再评估

当前桥接 skill 名称：`novel-ainovel-bridge`

可选备选名：

- `ainovel-bridge`
- `novel-bridge-ainovel`
- `novel-ainovel-handoff`

如果后续会出现多个 bridge，当前命名已经够清楚；如果不会，名字还可以再缩短。

## 建议顺序

推荐你后续按这个顺序做：

1. 补 bridge 测试
2. 细化 feed 字段规范
3. 实现 accepted 回流规则
4. 补 README 组合用法示例
5. 再考虑命名微调

## 判断是否需要继续改

如果当前目标只是：

- 保住 `novel` 通用性
- 把 AI-Novel 耦合剥出去

那现在已经够用。

如果目标是：

- 真正长期把 skill 和 AI-Novel 联机跑起来

那优先做 **bridge 测试 + 字段规范 + sync 规则**。
