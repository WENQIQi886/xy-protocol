# User Instruction Memory

This file records user instructions, preferences, and teachings for reference in future interactions.

## Format

### User Instruction Entry
User instruction entries should follow this format:

[User Instruction Summary]
- Date: [YYYY-MM-DD]
- Context: [Mentioned scenario or time]
- Instructions:
  - [Content of user teaching or instruction, described line by line]

### Project Knowledge Entry
Entries discovered by the Agent during task execution should follow this format:

[Project Knowledge Summary]
- Date: [YYYY-MM-DD]
- Context: Discovered by Agent while performing [specific task description]
- Category: [Operations & Deployment|Build Methods|Testing Methods|Troubleshooting & Debugging|Workflow & Collaboration|Environment Configuration]
- Instructions:
  - [Specific knowledge points, described line by line]

## Deduplication Strategy
- Before adding a new entry, check for similar or identical instructions.
- If a duplicate is found, skip the new entry or merge it with the existing one.
- When merging, update the context or date information.
- This helps avoid redundant entries and keeps the memory file tidy.

## Entries

[User Instruction Summary]
- Date: 2026-08-27
- Context: 用户要求对 param-imaging 开源仓库做同行对比与 QC 改善部署时，两次强调"要技术落地，不是讲一堆方案"
- Instructions:
  - 用户提出质量/管理方法类要求（如 QC 七大手法、六西格玛黑带、核工业标准）时，默认执行的是"直接落地到仓库工程文件"（CI/CD 流水线、Makefile 门禁、Dockerfile、校验脚本等），不要输出长篇方案/文档后再等确认
  - "继续"短指令在本会话中表示"推进当前未完成的落地任务"，应直接判断下一步动作并执行，不要反问

[Project Knowledge Summary]
- Date: 2026-08-27
- Context: Discovered by Agent while performing 跨设备（手机端 ↔ Linux 远程工作区）验证包复现套件落地
- Category: Environment Configuration
- Instructions:
  - 用户处于手机端，运行环境只能上传图片/文字，无法直接传输文件；文件内容需通过文字复刻或 base64（纯 ASCII，零失真）传入远程工作区
  - 原始验证包（15 个文件，约 110KB）完整保留在本机 `D:\param-imaging\validation_package_v2.0\`，若需与原始 manifest.json 哈希字节级对齐，只能走 base64 无损还原路径，转述复刻版不可能逐字节一致

[Project Knowledge Summary]
- Date: 2026-08-27
- Context: Discovered by Agent while performing 部署门禁与哈希口径确认
- Category: Operations & Deployment
- Instructions:
  - param-imaging 仓库哈希门禁口径：门禁要求"包内自洽可复现"，要求 `scripts/checksum.sh generate` 生成的哈希链能通过 `make verify`；不要求与历史 manifest.json 记录的 8 条 SHA-256 逐字节一致
  - 哈希链生成命令：在仓库根执行 `scripts/checksum.sh generate`；校验用 `make verify`；output JSON 含 `datetime.now()` 时间戳，每次复现哈希必然不同，属预期