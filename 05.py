import matplotlib.pyplot as plt
x_values = range(1,1000)
y_values = [x**2 for x in x_values]

fig, ax = plt.subplots()
ax.scatter(x_values,y_values,c=y_values, cmap=plt.cm.Blues,s=10)
ax.axis([0,1100,0, 1_100_000])
ax.ticklabel_format(style="plain")

plt.show()
plt.savefig("abcd.png",bbox_inches="tight")