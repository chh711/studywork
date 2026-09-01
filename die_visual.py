from matplotlib.pyplot import title
from pandas.tseries import frequencies

from die import Die
import plotly.express as px

die = Die()
results = []
for _ in range(1000):
    res = die.roll()
    results.append(res)

print(results)

frequencies = []
poss_results = range(1,die.num_sides+1)
for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)

print(frequencies)

title = "投掷骰子1000次的结果"
labels = {"x":"可能性","y":"出现的次数"}
fig = px.bar(
    x=poss_results,
    y=frequencies,
    title=title,
    labels=labels,
)

fig = px.bar(x=poss_results, y=frequencies)
fig.show()



