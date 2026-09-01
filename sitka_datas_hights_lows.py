from pathlib import Path
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# 绝对路径（避免工作目录问题）
script_dir = Path(__file__).parent
path = script_dir / 'weather_data' / 'sitka_weather_2021_simple.csv'

if not path.exists():
    print(f"文件不存在：{path.absolute()}")
    exit()

lines = path.read_text().splitlines()
reader = csv.reader(lines)
header_row = next(reader)   # 跳过标题行（关键！）

dates, highs = [], []
for row in reader:
    current_date = datetime.strptime(row[2], '%Y-%m-%d')
    dates.append(current_date)
    high = float(row[4])   # 改为 float
    highs.append(high)

plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(dates, highs, color='red')

ax.set_title('Daily High Temperatures, July 2021', fontsize=24)
ax.set_xlabel('', fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel('Temperature (F)', fontsize=16)
ax.tick_params(labelsize=16)

plt.show()
plt.show()