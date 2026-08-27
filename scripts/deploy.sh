#!/usr/bin/env bash
# ============================================================================
# 一键校验与构建入口（对齐 CI 门禁）
# 用法: ./scripts/deploy.sh [verify|build|check|all]
# ============================================================================
set -euo pipefail

ACTION="${1:-check}"

echo "==> Param Imaging 部署门禁（seed=0x612）"

case "${ACTION}" in
  verify)
    make verify
    ;;
  build)
    make build
    ;;
  check)
    make check
    ;;
  all)
    make check
    make test
    ;;
  *)
    echo "用法: $0 {verify|build|check|all}" >&2
    exit 1
    ;;
esac
