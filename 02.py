import matplotlib.pyplot as plt
x_values = [1, 2, 3, 4, 5]
y_values = [10, 20, 30, 40, 50]

fig, ax = plt.subplots()
ax.plot(x_values, y_values, linewidth=3)
ax.scatter(x_values, y_values,s=100)
ax.scatter(3,15, s= 100,c = 'red')
ax.scatter(4,19, s= 100,c = [(0.8,0,0)])

plt.show()
