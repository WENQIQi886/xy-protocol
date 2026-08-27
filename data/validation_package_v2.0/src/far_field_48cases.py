"""
far_field_48cases.py

远距极限验证 — 50m/100m 全因子组合 (48组)

6因子: 距离×模式×焦距×帧数×目标×光照

"""

import numpy as np

import json

from datetime import datetime

PIXEL_SIZE_M = 3.125e-6

# 26mm / 70mm / 120mm 等效 → 物理焦距 (1/1.7" sensor crop ~4.6x)

FOCAL_MAP = {

    '26mm':  {'f_mm': 4.5,  'label': '26mm主摄'},

    '70mm':  {'f_mm': 12.1, 'label': '70mm长焦'},

    '120mm': {'f_mm': 20.8, 'label': '120mm潜望'},

}

NOISE_MAP = {'良好': 1.0, '恶劣': 2.5}

TARGET_MAP = {'圆柱(Ø0.15m)': 0.15, '树木(冠6m)': 6.0}

TARGET_NOISE = {'圆柱(Ø0.15m)': 1.0, '树木(冠6m)': 1.4}

def angular_pixel_size(f_phys_mm):

    """单像素角分辨率 (mrad)"""

    return (PIXEL_SIZE_M / (f_phys_mm * 1e-3)) * 1000

def diameter_precision_angular(Z_m, f_phys_mm, N, noise_factor):

    """直径精度(角度法): σ_D = Z × θ_pixel × noise / √N  (mm)"""

    theta = angular_pixel_size(f_phys_mm) * 1e-3  # mrad → rad

    return Z_m * 1000 * theta / np.sqrt(N) * noise_factor

def depth_precision_stereo(Z_m, B_m, f_phys_mm, N, noise_factor):

    """深度精度: σ_Z = Z² × Δp / (B × f × √N) × noise  (mm)"""

    return (Z_m**2 * PIXEL_SIZE_M / (B_m * f_phys_mm * 1e-3 * np.sqrt(N))) * 1000 * noise_factor

def total_diameter_precision(Z_m, B_m, f_phys_mm, N, noise_factor, true_diameter_m):

    """综合: sqrt(角度² + 深度衍生²)"""

    sigma_ang = diameter_precision_angular(Z_m, f_phys_mm, N, noise_factor)

    sigma_dep = depth_precision_stereo(Z_m, B_m, f_phys_mm, N, noise_factor)

    sigma_dep_derived = sigma_dep * (true_diameter_m / Z_m)

    return sigma_ang, sigma_dep, np.sqrt(sigma_ang**2 + sigma_dep_derived**2)

def grade(error_pct):

    if error_pct < 0.5: return "S"

    elif error_pct < 1.5: return "A"

    elif error_pct < 3.3: return "B"

    elif error_pct < 5.0: return "C"

    else: return "F"

# ====== 全组合生成 ======

distances = [50.0, 100.0]

modes = [('全景', 2.5), ('实况', 0.5)]

focals = ['26mm', '70mm', '120mm']

frames = [200, 400]

targets = ['圆柱(Ø0.15m)', '树木(冠6m)']

lights = ['良好', '恶劣']

all_cases = []

cid = 0

for dist in distances:

    for mode_name, bl in modes:

        for fl_key in focals:

            for nf in frames:

                for tgt in targets:

                    for light in lights:

                        cid += 1

                        all_cases.append((f'F{cid}', dist, mode_name, bl, fl_key, nf, tgt, light))

print(f"  远距极限验证 — 48组全因子正交实验")

print(f"  覆盖: 50m/100m × 全景/实况 × 26/70/120mm × 200/400帧 × 圆柱/树木 × 良好/恶劣")

print("=" * 105)

results = []

# 分类统计

for cid, dist, mode_name, bl, fl_key, nf, tgt, light in all_cases:

    f_info = FOCAL_MAP[fl_key]

    noise = NOISE_MAP[light] * TARGET_NOISE[tgt]

    true_diam = TARGET_MAP[tgt]

    

    sigma_ang, sigma_dep, sigma_total = total_diameter_precision(

        dist, bl, f_info['f_mm'], nf, noise, true_diam

    )

    error_pct = round(sigma_total / (true_diam * 10), 4)  # mm → %

    g = grade(error_pct)

    passed = error_pct < 3.3

    

    # 毫米级判定 (圆柱150mm < 1mm, 树木6000mm < 30mm)

    mm_threshold = 1.0 if '圆柱' in tgt else 30.0

    is_mm = sigma_total < mm_threshold

    

    results.append({

        'id': cid, 'distance_m': dist, 'mode': mode_name, 'baseline_m': bl,

        'focal': fl_key, 'f_phys_mm': f_info['f_mm'], 'frames': nf,

        'target': tgt, 'true_diameter_m': true_diam,

        'lighting': light, 'noise_factor': round(noise, 2),

        'sigma_angular_mm': round(sigma_ang, 2), 'sigma_depth_mm': round(sigma_dep, 1),

        'sigma_total_mm': round(sigma_total, 2),

        'error_pct': error_pct, 'grade': g, 'passed': bool(passed),

        'millimeter_level': bool(is_mm)

    })

# 输出表格

header = f"{'ID':<4}{'距离':>5}{'模式':>4}{'焦距':>6}{'帧':>5}{'目标':<14}{'光照':>4}{'σ_角':>7}{'σ_深':>8}{'σ_总':>8}{'误差%':>7}{'评级':>5}{'毫米级':>6}"

print(header)

print("-" * 105)

for r in results:

    mm_label = '✅' if r['millimeter_level'] else '❌'

    print(f"{r['id']:<4}{r['distance_m']:>4.0f}m{r['mode']:>4}{r['focal']:>6}{r['frames']:>4} "

          f"{r['target']:<14}{r['lighting']:>4}"

          f"{r['sigma_angular_mm']:>6.1f}mm{r['sigma_depth_mm']:>7.0f}mm"

          f"{r['sigma_total_mm']:>7.2f}mm{r['error_pct']:>6.2f}%{r['grade']:>5}{mm_label:>6}")

# 汇总

print(f"\n{'='*105}")

passed_list = [r for r in results if r['passed']]

mm_list = [r for r in results if r['millimeter_level']]

print(f"\n  拉高50%标准(<3.3%)通过: {len(passed_list)}/48 = {len(passed_list)/48*100:.0f}%")

print(f"  毫米级通过: {len(mm_list)}/48 = {len(mm_list)/48*100:.0f}%")

grades_count = {g: sum(1 for r in results if r['grade'] == g) for g in ['S','A','B','C','F']}

print(f"  等级分布: S={grades_count['S']} A={grades_count['A']} B={grades_count['B']} C={grades_count['C']} F={grades_count['F']}")

# 按模式

print(f"\n  按模式:")

for mn in ['全景', '实况']:

    mr = [r for r in results if r['mode'] == mn]

    avg = np.mean([r['error_pct'] for r in mr])

    pct = sum(1 for r in mr if r['passed']) / len(mr) * 100

    print(f"    {mn}: 平均误差{avg:.2f}%  通过率{pct:.0f}%")

# 按焦距

print(f"\n  按焦距:")

for fl in ['26mm', '70mm', '120mm']:

    fr = [r for r in results if r['focal'] == fl]

    avg = np.mean([r['error_pct'] for r in fr])

    pct = sum(1 for r in fr if r['passed']) / len(fr) * 100

    mm_pct = sum(1 for r in fr if r['millimeter_level']) / len(fr) * 100

    print(f"    {fl}: 平均误差{avg:.2f}%  通过率{pct:.0f}%  毫米级{mm_pct:.0f}%")

# 按距离

print(f"\n  按距离:")

for d in [50.0, 100.0]:

    dr = [r for r in results if r['distance_m'] == d]

    avg = np.mean([r['error_pct'] for r in dr])

    pct = sum(1 for r in dr if r['passed']) / len(dr) * 100

    print(f"    {int(d)}m: 平均误差{avg:.2f}%  通过率{pct:.0f}%")

# 按目标

print(f"\n  按目标:")

for tgt_key, tgt_name in [('圆柱(Ø0.15m)', 'Ø15cm圆柱'), ('树木(冠6m)', '6m冠幅树木')]:

    tr = [r for r in results if r['target'] == tgt_key]

    avg = np.mean([r['error_pct'] for r in tr])

    pct = sum(1 for r in tr if r['passed']) / len(tr) * 100

    mm_pct = sum(1 for r in tr if r['millimeter_level']) / len(tr) * 100

    print(f"    {tgt_name}: 平均误差{avg:.2f}%  通过率{pct:.0f}%  毫米级{mm_pct:.0f}%")

# 关键发现

print(f"\n  失败用例分析:")

failed_list = [r for r in results if not r['passed']]

for r in failed_list:

    print(f"    [{r['id']}] {r['distance_m']:.0f}m-{r['mode']}-{r['focal']}-{r['frames']}帧-{r['target']}-{r['lighting']}: "

          f"σ={r['sigma_total_mm']:.2f}mm 误差={r['error_pct']:.2f}%")

if not failed_list:

    print(f"    (无) — 全部通过拉高50%标准")

# 最佳组合

best = sorted(results, key=lambda x: x['error_pct'])[:5]

print(f"\n  最佳5组合:")

for r in best:

    print(f"    [{r['id']}] {r['distance_m']:.0f}m-{r['mode']}-{r['focal']}-{r['frames']}帧-{r['target']}-{r['lighting']}: "

          f"σ={r['sigma_total_mm']:.2f}mm 误差={r['error_pct']:.2f}% {r['grade']}")

# 存档

output_path = "C:/Users/zhong/AppData/Roaming/Tencent/Marvis/User/oAN1i2afY0iez2OXrf8pvWGOxpI0/workspace/conv_19ec3f14866_5a3840815c6e/output/far_field_48cases_results.json"

archive = {

    'experiment': '远距极限验证 — 50m/100m全因子正交',

    'date': datetime.now().isoformat(),

    'standard': '拉高50%行业标准 (直径误差<3.3%)',

    'factors': {

        '距离': '50m / 100m',

        '模式': '全景(2.5m基线) / 实况(0.5m基线)',

        '焦距': '26mm主摄 / 70mm长焦 / 120mm潜望',

        '帧数': '200 / 400',

        '目标': '圆柱Ø15cm / 树木冠幅6m',

        '光照': '良好(×1.0) / 恶劣(×2.5)'

    },

    'total_cases': 48,

    'passed': len(passed_list),

    'pass_rate_pct': round(len(passed_list)/48*100, 1),

    'millimeter_passed': len(mm_list),

    'grade_distribution': grades_count,

    'results': results

}

with open(output_path, 'w', encoding='utf-8') as f:

    json.dump(archive, f, indent=2, ensure_ascii=False)

print(f"\n[存档] {output_path}")
