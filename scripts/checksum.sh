#!/usr/bin/env bash
# ============================================================================
# 数据哈希链生成/校验脚本（种子 0x612 驱动，HAF003 记录管理）
#
# 用法:
#   scripts/checksum.sh generate  生成 checksums.sha256
#   scripts/checksum.sh verify    校验 checksums.sha256
#   scripts/checksum.sh update    生成并覆盖
# ============================================================================
set -euo pipefail

DATA_DIR="data"
CHECKSUM_FILE="checksums.sha256"
ACTION="${1:-verify}"

case "${ACTION}" in
  generate|update)
    echo "==> 生成哈希链 ${CHECKSUM_FILE}"
    # 只对 data/ 下的实验产物生成哈希
    find "${DATA_DIR}" -type f ! -name 'README.md' -print0 \
      | sort -z \
      | xargs -0 sha256sum > "${CHECKSUM_FILE}"
    echo "==> 生成完成，共 $(wc -l < "${CHECKSUM_FILE}") 个文件"
    ;;
  verify)
    echo "==> 校验哈希链 ${CHECKSUM_FILE}"
    if [ ! -f "${CHECKSUM_FILE}" ]; then
      echo "[SKIP] ${CHECKSUM_FILE} 不存在，数据包上传后执行 generate"
      exit 0
    fi
    sha256sum -c "${CHECKSUM_FILE}"
    echo "==> 数据完整性校验通过"
    ;;
  *)
    echo "用法: $0 {generate|verify|update}" >&2
    exit 1
    ;;
esac
