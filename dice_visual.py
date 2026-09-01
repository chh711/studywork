import plotly.express as px
from die import Die
from die_visual import poss_results

die_1 = Die()
die_2 = Die()

# 生成数据
results = []
for _ in range(1000):
    res = die_1.roll() + die_2.roll()
    results.append(res)


# 统计分析

frequencies = []
max_results = die_1.num_sides + die_2.num_sides
poss_results = range(2,max_results +1 )
for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)

# 可视化
fig = px.bar(x=poss_results, y=frequencies)
fig.show()

fig.write_html("dice_visual.html")
