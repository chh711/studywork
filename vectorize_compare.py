"""
for 循环 vs numpy 向量化 性能对比
场景：对传感器数据进行统计（条件计数、分组均值、异常值检测）
"""

import numpy as np
import timeit
import os

# ── 生成模拟传感器数据（100 万条） ──────────────────────────────
np.random.seed(42)
N = 1_000_000
temperatures = np.random.normal(loc=25, scale=5, size=N)
humidity = np.random.normal(loc=70, scale=15, size=N)
humidity = np.clip(humidity, 0, 100)

print(f"数据规模：{N:,} 条\n")

# ══════════════════════════════════════════════════════════════
# 任务 1：统计温度 > 30°C 的条数
# ══════════════════════════════════════════════════════════════
print("=" * 55)
print("任务 1：统计温度 > 30°C 的条数")
print("=" * 55)

def count_loop():
    count = 0
    for v in temperatures:
        if v > 30:
            count += 1
    return count

def count_numpy():
    return np.sum(temperatures > 30)

t_loop = timeit.timeit(count_loop, number=5) / 5
t_np   = timeit.timeit(count_numpy, number=100) / 100
speedup = t_loop / t_np

print(f"  for 循环耗时：{t_loop*1000:.2f} ms  →  结果：{count_loop()}")
print(f"  numpy 耗时：  {t_np*1000:.4f} ms  →  结果：{count_numpy()}")
print(f"  加速比：{speedup:.1f}x")

# ══════════════════════════════════════════════════════════════
# 任务 2：计算温度均值和标准差
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("任务 2：计算温度均值和标准差")
print("=" * 55)

def stats_loop():
    s = 0.0
    for v in temperatures:
        s += v
    mean = s / len(temperatures)
    ss = 0.0
    for v in temperatures:
        ss += (v - mean) ** 2
    std = (ss / len(temperatures)) ** 0.5
    return mean, std

def stats_numpy():
    return np.mean(temperatures), np.std(temperatures)

t_loop = timeit.timeit(stats_loop, number=5) / 5
t_np   = timeit.timeit(stats_numpy, number=100) / 100
speedup = t_loop / t_np

mean_l, std_l = stats_loop()
mean_n, std_n = stats_numpy()
print(f"  for 循环耗时：{t_loop*1000:.2f} ms  →  均值={mean_l:.4f}, 标准差={std_l:.4f}")
print(f"  numpy 耗时：  {t_np*1000:.4f} ms  →  均值={mean_n:.4f}, 标准差={std_n:.4f}")
print(f"  加速比：{speedup:.1f}x")

# ══════════════════════════════════════════════════════════════
# 任务 3：异常值检测（温度超出 [mean-2*std, mean+2*std]）
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("任务 3：异常值检测（超出 2σ 范围）")
print("=" * 55)

def outlier_loop():
    mean = np.mean(temperatures)
    std = np.std(temperatures)
    lo, hi = mean - 2 * std, mean + 2 * std
    flags = np.zeros(N, dtype=bool)
    for i in range(N):
        if temperatures[i] < lo or temperatures[i] > hi:
            flags[i] = True
    return flags

def outlier_numpy():
    mean = np.mean(temperatures)
    std = np.std(temperatures)
    return (temperatures < mean - 2 * std) | (temperatures > mean + 2 * std)

t_loop = timeit.timeit(outlier_loop, number=3) / 3
t_np   = timeit.timeit(outlier_numpy, number=100) / 100
speedup = t_loop / t_np

print(f"  for 循环耗时：{t_loop*1000:.2f} ms  →  异常值：{np.sum(outlier_loop())} 条")
print(f"  numpy 耗时：  {t_np*1000:.4f} ms  →  异常值：{np.sum(outlier_numpy())} 条")
print(f"  加速比：{speedup:.1f}x")

# ══════════════════════════════════════════════════════════════
# 写入笔记
# ══════════════════════════════════════════════════════════════
note_path = os.path.join(os.path.dirname(__file__), "numpy_vectorize_notes.md")
with open(note_path, "w", encoding="utf-8") as f:
    f.write("# Numpy 向量化 vs For 循环 性能对比笔记\n\n")
    f.write(f"> 测试环境：{N:,} 条模拟传感器数据（温度、湿度）\n\n")
    f.write("## 测试结果\n\n")
    f.write("| 任务 | for 循环 | numpy 向量化 | 加速比 |\n")
    f.write("|------|---------|-------------|--------|\n")
    f.write(f"| 条件计数 (temp>30) | {t_loop*1000:.2f} ms | {t_np*1000:.4f} ms | **{speedup:.0f}x** |\n")

    # 重新跑一次任务2和3的计时用于笔记
    t2_loop = timeit.timeit(stats_loop, number=5) / 5
    t2_np   = timeit.timeit(stats_numpy, number=100) / 100
    t3_loop = timeit.timeit(outlier_loop, number=3) / 3
    t3_np   = timeit.timeit(outlier_numpy, number=100) / 100

    f.write(f"| 均值+标准差 | {t2_loop*1000:.2f} ms | {t2_np*1000:.4f} ms | **{t2_loop/t2_np:.0f}x** |\n")
    f.write(f"| 异常值检测 | {t3_loop*1000:.2f} ms | {t3_np*1000:.4f} ms | **{t3_loop/t3_np:.0f}x** |\n")

    f.write("\n## 结论\n\n")
    f.write("1. **numpy 向量化全面碾压 for 循环**，在百万级数据上加速比可达 **数十到数百倍**。\n")
    f.write("2. **根本原因**：for 循环在 Python 解释器中逐元素执行，每次迭代都有类型检查、对象创建等开销；\n")
    f.write("   numpy 在 C 层面批量操作连续内存数组，充分利用 CPU 缓存和 SIMD 指令。\n")
    f.write("3. **实践建议**：\n")
    f.write("   - 能用 numpy 内置函数（`np.sum`, `np.mean`, `np.std`）就不要写循环\n")
    f.write("   - 条件筛选用布尔索引（`arr[arr > 30]`）代替 `for + if`\n")
    f.write("   - 复杂逻辑优先考虑 `np.where`, `np.select`, 布尔掩码等向量化方案\n")
    f.write("   - 只有在逻辑无法向量化时，才考虑 `numba` JIT 或 `cython` 加速循环\n")

print(f"\n笔记已保存：{note_path}")
print("\n[OK] 对比完成！")
