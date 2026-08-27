"""
run_all.py — 奇玥验证引擎 V1.0 一键复现入口

python run_all.py

所有随机因子种子固定为 0x612，确保完全确定性复现。
"""

import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))

SRC = os.path.join(BASE, "src")

OUT = os.path.join(BASE, "output")

os.makedirs(OUT, exist_ok=True)

SCRIPTS = [

    ("orthogonal_validation.py", "基础正交 18组 (3-20m, 5因子)"),

    ("far_field_48cases.py",    "远距极限 96组 (50-100m, 6因子)"),

    ("user_env_18cases.py",     "三维生态 18组 (行为×环境×补强)"),

    ("angle_only_6cases.py",    "纯角度验证 6组 (3-20m, 深度切除)"),

]

print("=" * 64)

print("  奇玥验证引擎 V1.0 — 一键复现")

print(f"  种子: 0x612  实验: {len(SCRIPTS)} 个")

print("=" * 64)

for script, desc in SCRIPTS:

    path = os.path.join(SRC, script)

    print(f"\n[{desc}]")

    print(f"  脚本: {path}")

    

    if not os.path.exists(path):

        print(f"  [SKIP] 脚本不存在")

        continue

    

    # 读取并执行

    with open(path, 'r', encoding='utf-8') as f:

        code = f.read()

    

    # 修改输出路径指向 output/
    # 兼容: 完整 Windows 绝对路径 与 相对路径两种形式
    code = code.replace(
        'C:/Users/zhong/AppData/Roaming/Tencent/Marvis/User/oAN1i2afY0iez2OXrf8pvWGOxpI0/workspace/',
        ''
    ).replace(
        'C:\\\\Users\\\\zhong\\\\AppData\\\\Roaming\\\\Tencent\\\\Marvis\\\\User\\\\oAN1i2afY0iez2OXrf8pvWGOxpI0\\\\workspace\\\\',
        ''
    )
    code = code.replace(
        'conv_19ec3f14866_5a3840815c6e/output/',
        f'{OUT}/'
    ).replace(
        'conv_19ec3f14866_5a3840815c6e\\output\\',
        f'{OUT}\\'
    )

    

    exec(code)

    print(f"  完成.")

print(f"\n{'='*64}")

print(f"  全部实验完成。产出物目录: {OUT}")

print(f"  验证: sha256sum -c checksums.sha256")

print(f"{'='*64}")
