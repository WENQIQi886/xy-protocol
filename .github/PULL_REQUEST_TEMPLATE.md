---
name: 变更请求（Pull Request）
about: 提交代码变更前请填写此模板
title: '[类型] 简述变更内容'
labels: ''
assignees: ''
---

## 变更类型

- [ ] feat: 新功能
- [ ] fix: 缺陷修复
- [ ] docs: 文档
- [ ] chore: 构建/工具链
- [ ] test: 测试
- [ ] data: 验证数据变更

## 变更描述

<!-- 请清晰描述本次变更的内容与动机 -->

## 相关 Issue

<!-- 如有：Fixes #123 -->

## 门禁检查

- [ ] 已运行 `make check`，全部通过
- [ ] 涉及 `data/` 变更已同步更新 `checksums.sha256`
- [ ] 不包含专利核心算法/未脱敏材料
- [ ] Commit 消息遵循 Conventional Commits

## 测试情况

<!-- 描述验证方式：本地运行、CI、实验复现等 -->

## 附加说明

<!-- 其他需要 reviewer 关注的内容 -->
