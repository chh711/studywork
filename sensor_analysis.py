"""
传感器数据分析：清洗缺失值 → 按小时聚合 → 画出一天趋势图
数据来源：Open-Meteo 免费历史天气 API（北京，2025-08-13）
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
import os

# ──────────────────────────────────────────────
# 1. 下载公开传感器 CSV 数据（Open-Meteo 免费 API）
# ──────────────────────────────────────────────
print("=" * 50)
print("步骤 1：下载公开传感器数据（北京 2025-08-13）")
print("=" * 50)

url = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude=39.9042&longitude=116.4074"
    "&start_date=2025-08-13&end_date=2025-08-13"
    "&hourly=temperature_2m,relative_humidity_2m,dew_point_2m"
    "&timezone=Asia/Shanghai"
)

resp = requests.get(url, timeout=30)
resp.raise_for_status()
data_json = resp.json()

# 解析为 DataFrame
hourly = data_json["hourly"]
df = pd.DataFrame({
    "time": pd.to_datetime(hourly["time"]),
    "temperature": hourly["temperature_2m"],       # °C
    "humidity": hourly["relative_humidity_2m"],     # %
    "dew_point": hourly["dew_point_2m"],            # °C
})

# 保存原始 CSV
raw_csv = os.path.join(os.path.dirname(__file__), "sensor_raw.csv")
df.to_csv(raw_csv, index=False)
print(f"原始数据已保存：{raw_csv}")
print(f"原始数据条数：{len(df)}")
print(df.head(10))

# ──────────────────────────────────────────────
# 2. 清洗缺失值
# ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("步骤 2：清洗缺失值")
print("=" * 50)

print(f"清洗前缺失值统计：\n{df.isnull().sum()}")

# 删除含缺失值的行
df_clean = df.dropna().reset_index(drop=True)

print(f"\n清洗后缺失值统计：\n{df_clean.isnull().sum()}")
print(f"清洗后数据条数：{len(df_clean)}（删除了 {len(df) - len(df_clean)} 条）")

# 保存清洗后 CSV
clean_csv = os.path.join(os.path.dirname(__file__), "sensor_cleaned.csv")
df_clean.to_csv(clean_csv, index=False)
print(f"清洗后数据已保存：{clean_csv}")

# ──────────────────────────────────────────────
# 3. 按小时聚合（此处已是逐小时数据，演示聚合逻辑）
# ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("步骤 3：按小时聚合")
print("=" * 50)

# 设置时间索引，按小时重采样取均值
df_clean = df_clean.set_index("time")
df_hourly = df_clean.resample("1h").mean()

# 保存聚合后 CSV
agg_csv = os.path.join(os.path.dirname(__file__), "sensor_hourly.csv")
df_hourly.to_csv(agg_csv)
print(f"按小时聚合数据已保存：{agg_csv}")
print(df_hourly)

# ──────────────────────────────────────────────
# 4. 绘制一天趋势图并保存
# ──────────────────────────────────────────────
print("\n" + "=" * 50)
print("步骤 4：绘制趋势图")
print("=" * 50)

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

fig, ax1 = plt.subplots(figsize=(12, 5))

# 温度曲线（左轴）
color_temp = "#e74c3c"
ax1.set_xlabel("时间（小时）", fontsize=12)
ax1.set_ylabel("温度 (°C)", color=color_temp, fontsize=12)
line1 = ax1.plot(
    df_hourly.index, df_hourly["temperature"],
    color=color_temp, marker="o", linewidth=2, markersize=5,
    label="温度 (°C)"
)
ax1.tick_params(axis="y", labelcolor=color_temp)
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax1.set_title("北京 2025-08-13 温湿度传感器日趋势", fontsize=14, fontweight="bold")
ax1.grid(True, alpha=0.3)

# 湿度曲线（右轴）
ax2 = ax1.twinx()
color_hum = "#3498db"
ax2.set_ylabel("相对湿度 (%)", color=color_hum, fontsize=12)
line2 = ax2.plot(
    df_hourly.index, df_hourly["humidity"],
    color=color_hum, marker="s", linewidth=2, markersize=5,
    label="相对湿度 (%)"
)
ax2.tick_params(axis="y", labelcolor=color_hum)

# 图例
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper right", fontsize=10)

plt.tight_layout()

# 保存图片
fig_path = os.path.join(os.path.dirname(__file__), "sensor_trend.png")
fig.savefig(fig_path, dpi=150, bbox_inches="tight")
print(f"趋势图已保存：{fig_path}")
plt.close()

print("\n[OK] 全部完成！生成文件：")
print("   - sensor_raw.csv     -- 原始数据")
print("   - sensor_cleaned.csv -- 清洗后数据")
print("   - sensor_hourly.csv  -- 按小时聚合数据")
print("   - sensor_trend.png   -- 一天趋势图")



