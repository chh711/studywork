import matplotlib.pyplot as plt
from random_walk import RandomWalk

rw = RandomWalk()
rw.fill_walk()
plt.style.use("classic")

fig, ax = plt.subplots(figsize=(13.95,7.84),dpi=128)

ax.scatter(
    rw.x_values,
    rw.y_values,
    c=range(rw.num_points),
    cmap=plt.cm.Blues,
    edgecolors="none",
    s=10,
)

ax.set_aspect("equal")

ax.scatter(0,0,c="green",edgecolors="none",s=100)
ax.scatter(rw.x_values[-1],rw.y_values[-1],c="red",edgecolors="none",s=100)


ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

plt.show()