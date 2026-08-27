# 验证数据包（Validation Package）

本目录包含 `validation_package_v2.0` 实验数据，与专利申请号 `202611094798.X` 对应。

## 目录结构

```
validation_package_v2.0/
├── README.txt              # 运行说明+实验清单
├── run_all.py              # 一键复现入口
├── manifest.json           # 环境指纹+元数据
├── experiment_summary.txt  # 实验摘要
├── src/                    # 实验脚本（正交/远距/三维生态/纯角度）
│   ├── orthogonal_validation.py
│   ├── far_field_48cases.py
│   ├── user_env_18cases.py
│   └── angle_only_6cases.py
├── configs/                # 实验配置文件（正交实验配置 JSON）
└── output/                 # 实验数据结果（4 个结果 JSON）
    ├── orthogonal_18cases_results.json
    ├── far_field_48cases_results.json
    ├── user_env_18cases_results.json
    └── angle_only_6cases_results.json
```

## 使用说明

```bash
# 1. 校验数据完整性（哈希链校验）
make verify
# 或
scripts/checksum.sh verify

# 2. 一键复现实验（在验证包目录内）
cd data/validation_package_v2.0
python run_all.py

# 3. 数据变更后重新生成哈希链
scripts/checksum.sh generate
```

## 实验摘要

- **总实验数**：120 组（基础正交 18 + 远距极限 96 + 三维生态 18 + 纯角度验证 6）
- **核心实验**：
  - A3：线性化公式修正（远距误差修正）
  - B：短基线远距失效机理（基线与视差关系）
  - D：测距测径解耦（0.47% vs 127.8%）
  - G：六路线横向对比（变焦融合、纯角度法）

## 当前状态（2026-08）

已落地完整复现套件（12 个文件）：

```
validation_package_v2.0/
├── README.txt                  ✅
├── run_all.py                  ✅ 一键复现入口（已兼容 Windows 绝对路径替换）
├── manifest.json               ✅ 环境指纹+元数据
├── experiment_summary.txt      ✅ 实验摘要
├── src/                        ✅ 4 个实验脚本（已可运行）
│   ├── orthogonal_validation.py
│   ├── far_field_48cases.py
│   ├── user_env_18cases.py
│   └── angle_only_6cases.py
└── output/                     ✅ 4 个结果 JSON（复现生成）
    ├── orthogonal_18cases_results.json
    ├── far_field_48cases_results.json
    ├── user_env_18cases_results.json
    └── angle_only_6cases_results.json
```

> **哈希一致性说明（重要）**：`manifest.json` 内记录的 8 条 SHA-256 来自原始机器文件。本仓库文件经手机端转述复刻，字节级存在差异，且 output JSON 含运行时时间戳（`datetime.now()`），因此当前哈希链与 manifest 记录**不一致**。`checksums.sha256` 已基于当前 12 个文件重新生成并自洽校验通过。若需与原始包逐字节对齐，须以原始文件覆盖后重新 `scripts/checksum.sh generate`。

## 复现验证

```bash
cd data/validation_package_v2.0
python run_all.py          # 生成 output/ 下 4 个 JSON
cd ../.. && make verify    # 校验哈希链
```

## 专利关联

本验证数据包是专利申请号 `202611094798.X` 的配套实验证据，用于证明本方法的性能优势。种子 `0x612` 驱动全部随机因子，保证确定性复现。
