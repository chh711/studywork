import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUTDIR = Path('outputs')
OUTDIR.mkdir(exist_ok=True)


def rolling_stats(x: np.ndarray, window: int):
    """Causal rolling mean/std using the previous `window` points (excluding current)."""
    n = len(x)
    means = np.full(n, np.nan)
    stds = np.full(n, np.nan)

    csum = np.cumsum(np.insert(x, 0, 0.0))
    csum2 = np.cumsum(np.insert(x * x, 0, 0.0))

    for i in range(window, n):
        s = csum[i] - csum[i - window]
        s2 = csum2[i] - csum2[i - window]
        mean = s / window
        var = max(s2 / window - mean * mean, 0.0)
        means[i] = mean
        stds[i] = math.sqrt(var)
    return means, stds


def normal_rule_demo(seed: int = 42):
    rng = np.random.default_rng(seed)
    samples = rng.normal(loc=0.0, scale=1.0, size=10_000)
    mean = samples.mean()
    std = samples.std(ddof=0)

    levels = [1, 2, 3]
    within = {}
    for k in levels:
        within[k] = float(np.mean(np.abs(samples - mean) <= k * std))

    print('=== 正态分布 68-95-99.7 规则验证 ===')
    print(f'样本均值: {mean:.4f}, 样本标准差: {std:.4f}')
    for k in levels:
        theory = {1: 0.6827, 2: 0.9545, 3: 0.9973}[k]
        print(f'±{k}σ 内比例: {within[k]*100:.2f}%  (理论约 {theory*100:.2f}%)')

    xs = np.linspace(mean - 4 * std, mean + 4 * std, 500)
    pdf = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((xs - mean) / std) ** 2)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(samples, bins=40, density=True, alpha=0.65, color='#4C78A8', edgecolor='white', label='样本直方图')
    ax.plot(xs, pdf, color='#F58518', lw=2.5, label='拟合正态曲线')
    for k, color in zip(levels, ['#54A24B', '#E45756', '#B279A2']):
        ax.axvline(mean + k * std, color=color, ls='--', lw=1.4)
        ax.axvline(mean - k * std, color=color, ls='--', lw=1.4)
    ax.set_title('10000 个正态样本与 68-95-99.7 规则')
    ax.set_xlabel('数值')
    ax.set_ylabel('密度')
    ax.legend()
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUTDIR / 'normal_rule_demo.png', dpi=160)
    plt.close(fig)

    return {
        'mean': mean,
        'std': std,
        'within_1sigma': within[1],
        'within_2sigma': within[2],
        'within_3sigma': within[3],
    }


def anomaly_detection_demo(seed: int = 123):
    rng = np.random.default_rng(seed)
    n = 240
    t = np.arange(n)
    baseline = 20 + 0.04 * t + 1.5 * np.sin(t / 10)
    noise = rng.normal(0, 0.8, size=n)
    sensor = baseline + noise

    anomaly_idx = np.array([35, 74, 121, 166, 210])
    sensor[anomaly_idx] += np.array([7, -6, 8, -7, 9])

    window = 24
    means, stds = rolling_stats(sensor, window)
    z = np.abs(sensor - means) / stds
    anomalies = (z > 3) & np.isfinite(z)

    print('\n=== 3σ 异常检测 ===')
    print(f'窗口大小: {window}')
    print(f'标记异常点数: {int(anomalies.sum())}')
    print('异常点索引:', np.where(anomalies)[0].tolist())

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(t, sensor, color='#4C78A8', lw=1.6, label='传感器数据')
    ax.plot(t, means, color='#F58518', lw=2.0, label='滑动均值')
    ax.fill_between(t, means - 3 * stds, means + 3 * stds, color='#F58518', alpha=0.15, label='±3σ 区间')
    ax.scatter(t[anomalies], sensor[anomalies], color='#E45756', s=55, zorder=5, label='异常点')
    ax.set_title('基于滑动均值/标准差的 3σ 异常检测')
    ax.set_xlabel('时间')
    ax.set_ylabel('传感器读数')
    ax.legend(ncol=4, fontsize=9)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUTDIR / 'anomaly_detection_demo.png', dpi=160)
    plt.close(fig)

    return {
        'window': window,
        'anomaly_indices': np.where(anomalies)[0].tolist(),
        'anomaly_count': int(anomalies.sum()),
    }


if __name__ == '__main__':
    normal_stats = normal_rule_demo()
    anomaly_stats = anomaly_detection_demo()

    report = [
        '=== 结果摘要 ===',
        f"正态样本均值: {normal_stats['mean']:.4f}",
        f"正态样本标准差: {normal_stats['std']:.4f}",
        f"±1σ 覆盖率: {normal_stats['within_1sigma']*100:.2f}%",
        f"±2σ 覆盖率: {normal_stats['within_2sigma']*100:.2f}%",
        f"±3σ 覆盖率: {normal_stats['within_3sigma']*100:.2f}%",
        f"3σ 异常点数: {anomaly_stats['anomaly_count']}",
        f"异常点索引: {anomaly_stats['anomaly_indices']}",
    ]
    (OUTDIR / 'results.txt').write_text('\n'.join(report), encoding='utf-8')
    print(f'\n图片与结果已保存到: {OUTDIR.resolve()}')
