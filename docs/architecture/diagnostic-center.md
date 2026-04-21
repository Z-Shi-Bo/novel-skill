# Diagnostic Center

## 目标

把 diagnose 从“脚本式查错”升级为“诊断中心”。

## 当前层级

- chapter diagnose
- project diagnose
- trend diagnose（基础）
- stale hook diagnose（基础）
- continuity risk diagnose（基础）

## 输出

- Markdown：给人看
- JSON：给程序消费

## 设计原则

1. 先形成稳定字段，再扩复杂度。
2. 先把严重度汇总做稳。
3. 诊断结果必须能被 CLI 和自动化流程消费。
