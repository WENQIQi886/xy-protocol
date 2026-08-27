# 变更日志（Changelog）

本项目遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/) 与 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/) 规范。

## [未发布] (Unreleased)

### Added
- 多阶段 Dockerfile 构建（依赖层缓存 + 运行时瘦身）
- GitHub Actions CI 流水线：数据哈希校验、依赖锁定检查、镜像构建冒烟
- CodeQL 安全扫描（每周定时）
- Dependabot 依赖更新
- Release 自动发布流水线（SemVer 标签触发，推 GHCR 镜像）
- Makefile 工程命令（`make check/verify/build/test`）
- 依赖锁定 `requirements.txt`
- 社区规范：CONTRIBUTING / CODE_OF_CONDUCT / SECURITY
- Issue/PR 模板

### Changed
- `docs/experiments.md` 补充 A3/B/D/G 实验详情
- `data/README.md` 补充验证包目录结构与使用说明

### Fixed
- Dockerfile 改为非 root 运行（纵深防御）
