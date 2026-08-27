"""
user_env_18cases.py

用户行为 × 环境场景 × 补强路径 — 18组正交验证

"""

import numpy as np

import json

from datetime import datetime

PIXEL_SIZE_M = 3.125e-6

# 焦距映射

FOCAL_MAP = {

    '70mm':  12.1e-3,

    '120mm': 20.8e-3,

}

# 行为 → (基准基线m, 帧数, 行为噪声)

BEHAVIOR = {

    'U1_定点微动':   {'B': 0.10, 'frames': 30,  'noise': 1.0},

    'U2_原地平移':   {'B': 0.45, 'frames': 60,  'noise': 1.1},

    'U3_全景慢速':   {'B': 2.0,  'frames': 90,  'noise': 1.2},

    'U4_全景快速':   {'B': 2.5,  'frames': 60,  'noise': 1.5},

    'U5_行走慢走':   {'B': 4.0,  'frames': 120, 'noise': 1.8},

    'U6_行走快走':   {'B': 5.0,  'frames': 60,  'noise': 2.5},

}

# 环境 → 退化因子

ENV = {

    'E1_晴天': 1.0,

    'E2_阴天': 1.5,

    'E3_逆光': 2.5,

    'E4_雨雾': 4.0,

}

# 目标 → (直径m, 目标噪声)

TARGET = {

    '树木_冠6m':    (6.0,  1.4),

    '建筑_宽15m':   (15.0, 1.0),

}

# 补强 → 基线覆写 (None=保留行为基线)

BOOST_BASELINE = {

    'P1_行走基线':   None,     # 保留行为基线

    'P2_长焦双摄':   0.015,    # 主摄-长焦物理基线15mm

    'P3_多设备协同': 5.0,      # 双手机5m

}

def angular_resolution(f_m):

    return PIXEL_SIZE_M / f_m

def sigma_diameter_angular(Z_m, f_m, N, noise):

    return Z_m * 1000 * angular_resolution(f_m) / np.sqrt(N) * noise

def sigma_depth_stereo(Z_m, B_m, f_m, N, noise):

    return (Z_m**2 * PIXEL_SIZE_M / (B_m * f_m * np.sqrt(N))) * 1000 * noise

def total_sigma_diameter(Z_m, B_m, f_m, N, noise, true_diam):

    sa = sigma_diameter_angular(Z_m, f_m, N, noise)

    sd = sigma_depth_stereo(Z_m, B_m, f_m, N, noise)

    sd_d = sd * (true_diam / Z_m)

    return sa, sd, np.sqrt(sa**2 + sd_d**2)

def grade(pct):

    if pct < 0.5: return "S"

    elif pct < 1.5: return "A"

    elif pct < 3.3: return "B"

    elif pct < 5.0: return "C"

    else: return "F"

# 18组核心用例

cases = [

    ("UE1",  "U1_定点微动", "E1_晴天", "树木_冠6m",  "P2_长焦双摄",  10,  "70mm"),

    ("UE2",  "U1_定点微动", "E3_逆光", "建筑_宽15m", "P2_长焦双摄",  20,  "120mm"),

    ("UE3",  "U2_原地平移", "E2_阴天", "树木_冠6m",  "P2_长焦双摄",  10,  "70mm"),

    ("UE4",  "U2_原地平移", "E4_雨雾", "建筑_宽15m", "P2_长焦双摄",  20,  "120mm"),

    ("UE5",  "U3_全景慢速", "E1_晴天", "树木_冠6m",  "P1_行走基线",  50,  "120mm"),

    ("UE6",  "U3_全景慢速", "E3_逆光", "建筑_宽15m", "P3_多设备协同", 50,  "120mm"),

    ("UE7",  "U4_全景快速", "E2_阴天", "树木_冠6m",  "P1_行走基线",  50,  "70mm"),

    ("UE8",  "U4_全景快速", "E4_雨雾", "建筑_宽15m", "P3_多设备协同", 100, "120mm"),

    ("UE9",  "U5_行走慢走", "E1_晴天", "树木_冠6m",  "P1_行走基线",  50,  "120mm"),

    ("UE10", "U5_行走慢走", "E3_逆光", "建筑_宽15m", "P3_多设备协同", 100, "120mm"),

    ("UE11", "U6_行走快走", "E2_阴天", "树木_冠6m",  "P1_行走基线",  50,  "120mm"),

    ("UE12", "U6_行走快走", "E4_雨雾", "建筑_宽15m", "P3_多设备协同", 100, "70mm"),

    ("UE13", "U3_全景慢速", "E1_晴天", "树木_冠6m",  "P2_长焦双摄",  10,  "70mm"),

    ("UE14", "U4_全景快速", "E3_逆光", "建筑_宽15m", "P2_长焦双摄",  20,  "120mm"),

    ("UE15", "U5_行走慢走", "E1_晴天", "树木_冠6m",  "P3_多设备协同", 50,  "120mm"),

    ("UE16", "U6_行走快走", "E2_阴天", "建筑_宽15m", "P2_长焦双摄",  20,  "70mm"),

    ("UE17", "U3_全景慢速", "E4_雨雾", "树木_冠6m",  "P1_行走基线",  50,  "120mm"),

    ("UE18", "U5_行走慢走", "E4_雨雾", "建筑_宽15m", "P1_行走基线",  100, "120mm"),

]

print("=" * 100)

print("  用户行为 × 环境场景 × 补强路径 — 18组正交验证")

print("  6行为 × 4环境 × 3补强 — 拉高50%标准 (<3.3%)")

print("=" * 100)

results = []

for cid, beh, env, tgt, boost, dist, fl in cases:

    b_info = BEHAVIOR[beh]

    f_m = FOCAL_MAP[fl]

    true_diam, t_noise = TARGET[tgt]

    env_noise = ENV[env]

    

    # 基线选择: 补强覆写 > 行为基线

    B_m = BOOST_BASELINE[boost]

    if B_m is None:

        B_m = b_info['B']

    

    N = b_info['frames']

    noise = env_noise * b_info['noise'] * t_noise

    

    sa, sd, st = total_sigma_diameter(dist, B_m, f_m, N, noise, true_diam)

    err_pct = round(st / (true_diam * 10), 4)

    g = grade(err_pct)

    passed = err_pct < 3.3

    

    results.append({

        'id': cid, 'behavior': beh, 'environment': env, 'target': tgt,

        'boost': boost, 'distance_m': dist, 'focal': fl,

        'baseline_m': round(B_m, 3), 'frames': N, 'noise_total': round(noise, 2),

        'sigma_ang_mm': round(sa, 2), 'sigma_dep_mm': round(sd, 1),

        'sigma_total_mm': round(st, 2), 'error_pct': err_pct,

        'grade': g, 'passed': bool(passed)

    })

# 输出表格

hdr = f"{'ID':<5}{'行为':<14}{'环境':<10}{'目标':<12}{'补强':<12}{'距':>5}{'焦距':>6}{'B':>7}{'帧':>5}{'噪声':>6}{'σ角':>7}{'σ深':>8}{'σ总':>7}{'误差%':>7}{'评级':>5}"

print(hdr)

print("-" * 100)

for r in results:

    b_label = f"{r['baseline_m']:.3f}m" if r['baseline_m'] < 1.0 else f"{r['baseline_m']:.1f}m"

    print(f"{r['id']:<5}{r['behavior']:<14}{r['environment']:<10}{r['target']:<12}{r['boost']:<12}"

          f"{r['distance_m']:>4.0f}m{r['focal']:>6}{b_label:>7}{r['frames']:>4}"

          f"{r['noise_total']:>5.1f}x{r['sigma_ang_mm']:>6.1f}mm{r['sigma_dep_mm']:>7.0f}mm"

          f"{r['sigma_total_mm']:>6.2f}mm{r['error_pct']:>6.2f}%{r['grade']:>5}")

# 汇总

print(f"\n{'='*100}")

passed = [r for r in results if r['passed']]

failed = [r for r in results if not r['passed']]

gc = {g: sum(1 for r in results if r['grade'] == g) for g in ['S','A','B','C','F']}

print(f"\n  拉高50%标准通过: {len(passed)}/18 = {len(passed)/18*100:.0f}%")

print(f"  等级: S={gc['S']} A={gc['A']} B={gc['B']} C={gc['C']} F={gc['F']}")

# 按补强

print(f"\n  按补强路径:")

for boost_name in ['P1_行走基线', 'P2_长焦双摄', 'P3_多设备协同']:

    br = [r for r in results if r['boost'] == boost_name]

    avg = np.mean([r['error_pct'] for r in br])

    pct = sum(1 for r in br if r['passed']) / len(br) * 100

    print(f"    {boost_name}: 平均误差{avg:.2f}%  通过率{pct:.0f}%")

# 按行为

print(f"\n  按行为:")

for beh_name in BEHAVIOR:

    br = [r for r in results if r['behavior'] == beh_name]

    if br:

        avg = np.mean([r['error_pct'] for r in br])

        print(f"    {beh_name}: 平均误差{avg:.2f}%")

# 按环境

print(f"\n  按环境:")

for env_name in ENV:

    er = [r for r in results if r['environment'] == env_name]

    if er:

        avg = np.mean([r['error_pct'] for r in er])

        print(f"    {env_name}: 平均误差{avg:.2f}%")

# 失败详情

if failed:

    print(f"\n  未通过:")

    for r in failed:

        print(f"    [{r['id']}] {r['behavior']}|{r['environment']}|{r['target']}|{r['boost']} "

              f"σ={r['sigma_total_mm']:.2f}mm {r['error_pct']:.2f}%")

# 对比: P2 vs P1/P3 在近距和远距

print(f"\n  补强对比:")

for boost in ['P2_长焦双摄', 'P1_行走基线', 'P3_多设备协同']:

    br = [r for r in results if r['boost'] == boost]

    near = [r for r in br if r['distance_m'] <= 20]

    far = [r for r in br if r['distance_m'] >= 50]

    if near:

        print(f"    {boost} 近距(≤20m): avg_err={np.mean([x['error_pct'] for x in near]):.2f}%")

    if far:

        print(f"    {boost} 远距(≥50m): avg_err={np.mean([x['error_pct'] for x in far]):.2f}%")

output_path = "C:/Users/zhong/AppData/Roaming/Tencent/Marvis/User/oAN1i2afY0iez2OXrf8pvWGOxpI0/workspace/conv_19ec3f14866_5a3840815c6e/output/user_env_18cases_results.json"

archive = {

    'experiment': '用户行为×环境场景×补强路径 — 真实世界三维生态验证',

    'date': datetime.now().isoformat(),

    'standard': '拉高50%行业标准 (误差<3.3%)',

    'total': 18,

    'passed': len(passed),

    'pass_rate': f"{len(passed)/18*100:.0f}%",

    'grade_dist': gc,

    'results': results

}

with open(output_path, 'w', encoding='utf-8') as f:

    json.dump(archive, f, indent=2, ensure_ascii=False)

print(f"\n[存档] {output_path}")
