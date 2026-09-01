import matplotlib.pyplot as plt
x_values = [1, 2, 3, 4, 5]
y_values = [1, 4, 9, 16, 25]

plt.style.use('seaborn-v0_8')

fig, ax = plt.subplots()
ax.plot(x_values, y_values, linewidth=3)
ax.scatter(x_values, y_values,s=100)
ax.scatter(3,14, s= 100,c = 'red')

ax.set_xlabel('X-xxx',fontsize = 14)
ax.set_ylabel('Yyyy',fontsize = 14)
ax.set_title('Title',fontsize = 24)
ax.tick_params(labelsize=14)

plt.show()
