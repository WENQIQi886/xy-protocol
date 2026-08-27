================================================================================
  奇玥验证引擎 V1.0 — 取证级仿真测试套件
  Qiyue Validation Engine — Forensic Simulation Test Suite
================================================================================
  用途：为专利审查提供可复现的测量精度验证数据
  方法：确定性随机种子 + 纯数学物理模型 + SHA-256 哈希链
  标准：拉高 50% 行业标准（直径误差 < 3.3%）


【环境要求】
  · Python 3.8+
  · numpy
  · 无需 Blender、无需 GPU、无需 CUDA
  · 全部实验为纯数学仿真，可在任意操作系统运行


【一键复现】
  cd validation_package_v1.0/
  pip install numpy
  python run_all.py
  执行后将在 output/ 目录生成 4 个结果 JSON 文件，
  其 SHA-256 应与 checksums.sha256 中记载的完全一致。


【验证哈希一致性】
  # Windows
  certutil -hashfile output/orthogonal_18cases_results.json SHA256
  # Linux / macOS
  sha256sum -c checksums.sha256


【实验清单】
  ┌─────────────────────────────────────────────────────────────┐
  │ 实验               范围      因子     组数  通过率  关键发现 │
  ├─────────────────────────────────────────────────────────────┤
  │ 基础正交          3-20m      5       18    94%   全景S级   │
  │ 远距极限          50-100m    6       96    91.7%  70mm+全通│
  │ 三维生态验证       10-100m    6×4×3   18    67%→100%       │
  │ 纯角度验证         3-20m      4        6    100%S  全S级   │
  │ ─────────────────────────────────────────                   │
  │ 合计              3-100m     —      138    综合覆盖         │
  └─────────────────────────────────────────────────────────────┘
  注：三维生态验证中 P2（长焦双摄）因 15mm 基线对深度破坏，
      切除深度链路修正后通过率 100%。详见报告。


【确定性保证】
  所有实验使用 numpy.random.RandomState(0x612) 统一种子。
  无时间戳、无系统随机数、无硬件相关操作。
  任何人、任何设备、任何时间运行同一脚本，必得同一结果。


【文件结构】
  validation_package_v1.0/
  ├── README.txt                         本说明
  ├── run_all.py                         一键复现入口
  ├── checksums.sha256                   SHA-256 哈希清单
  ├── manifest.json                      取证级元数据+环境指纹
  ├── experiment_summary.txt             120组实验摘要
  ├── configs/
  │   └── (正交实验配置 JSON — 待生成)
  ├── src/
  │   ├── orthogonal_validation.py      基础正交 18 组
  │   ├── far_field_48cases.py          远距极限 96 组
  │   ├── user_env_18cases.py           三维生态 18 组
  │   └── angle_only_6cases.py          纯角度验证 6 组
  └── output/
      ├── orthogonal_18cases_results.json
      ├── far_field_48cases_results.json
      ├── user_env_18cases_results.json
      └── angle_only_6cases_results.json


【全局随机种子】
  SEED = 0x612
  含义：六一二，奇玥验证的锚点。
  所有微动轨迹、噪声注入、帧间抖动均由此种子派生。


【联系与存档】
  本包生成时间见 manifest.json 中 generated_at 字段。
  建议与本 checksums.sha256 一同存入网盘/光盘/区块链，
  作为不可篡改的电子证据。
================================================================================
  End of README
================================================================================
