# 贡献指南（Contributing Guide）

感谢您对 Param Imaging 的关注。本仓库遵循专利合规与开源协作的双重要求，请先阅读本文再提交贡献。

## 仓库边界

本仓库仅开源**验证数据、复现环境配置与实验报告**。以下内容**不随仓库分发**：

- 核心算法实现（时序预标定、变焦融合逻辑、纯角度法解耦）
- 未脱敏的专利原始材料
- 验证数据包本体（按需单独分发，见 `data/README.md`）

## 提交规范

### Commit 消息

使用 Conventional Commits 规范：

```
feat: 新增内容
fix: 修复问题
docs: 仅文档变更
chore: 构建/工具链变更
test: 测试变更
```

示例：`docs: 补充 A3 实验置信区间说明`

### 分支规范

- `main`：稳定分支，受保护，禁止直接推送
- 功能分支：`feat/<描述>`、`fix/<描述>`

## 开发流程

### 环境准备

```bash
# 1. 校验数据哈希（如已上传验证包）
make verify

# 2. 全量门禁（依赖 + 数据 + 构建）
make check

# 3. 构建镜像
make build
```

### PR 流程

1. 从 `main` 切出功能分支
2. 修改后运行 `make check` 通过全部门禁
3. 提交 PR，填写 PR 模板
4. 通过 CI（`verify-data`、`lint-deps`、`docker-build`）后才能合并

## 数据校验原则

任何涉及 `data/` 的改动必须同步更新 `checksums.sha256`，保持证据链完整（种子 `0x612` 驱动）。

## 许可证

提交即表示您同意 Apache License 2.0 条款。注意：本仓库不构成专利实施许可，商业实施需另行取得专利权人授权。
