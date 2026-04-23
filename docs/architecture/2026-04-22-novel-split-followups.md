# novel skill 三层拆分后续修改清单

日期：2026-04-22

## 当前已完成

- `novel` 恢复为通用全功能小说 skill
- `novel-framework` 新建为纯框架 skill
- `novel-ainovel-bridge` 保持为 AI-Novel 专属桥接层
- 根 README 与各 skill README 已更新
- smoke / guardrail 回归已通过（针对 `novel`）

## 后续建议修改

### P1：为 `novel-framework` 补最小回归测试

建议新增：

1. `framework smoke init`
2. `framework outline only`
3. `framework` 遇到“写正文”请求时应明确拒绝并提示用 `novel`

### P1：bridge 的 export / sync 细化

1. 明确 AI-Novel 当前真实消费字段与文件名
2. 把 `ainovel_feed` 模板从占位模板升级成“字段级规范”
3. 明确 `sync` 时哪些 accepted 结果可回流：
   - summary
   - pending hooks
   - current state
   - timeline
   - relationship changes

### P1：统一三层之间的 schema

重点统一：

- chapter context
- current state
- pending hooks
- outline entry
- character card

避免 `novel` / `novel-framework` / `bridge` 三边未来漂移。

### P2：README 增加组合用法示例

建议补一个最小示例：

1. `$novel-framework init`
2. `$novel-framework brief`
3. `$novel-framework bible`
4. `$novel-framework outline`
5. `$novel-ainovel-bridge export`
6. AI-Novel 跑正文
7. `$novel-ainovel-bridge sync`

再补一个全功能示例：

1. `$novel init`
2. `$novel brief`
3. `$novel outline`
4. `$novel write`
5. `$novel review`

### P2：桥接层测试 fixture

建议新增：

- 一个完整 `novel` 控制面 fixture
- 一个完整 `novel-framework` 控制面 fixture
- 一个 AI-Novel accepted fixture
- 一个 AI-Novel draft-only fixture

### P3：命名再评估

当前名称：

- `novel`
- `novel-framework`
- `novel-ainovel-bridge`

可选再评估：

- `novel-framework` 是否要叫 `novel-planner`
- `novel-ainovel-bridge` 是否要缩短成 `ainovel-bridge`

## 建议顺序

推荐后续按这个顺序做：

1. 补 `novel-framework` 测试
2. 细化 bridge 字段规范
3. 实现 accepted 回流规则
4. 补 README 组合示例
5. 再考虑命名微调

## 判断是否需要继续改

如果当前目标只是：

- `novel` 保持全功能
- 同时提供一个纯框架入口
- 把 AI-Novel 耦合固定在 bridge

那现在已经够用。

如果目标是：

- 长期稳定联动 `novel-framework` + AI-Novel

那优先做：

- framework 测试
- bridge 测试
- 字段级规范
