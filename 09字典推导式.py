# 以数字1-9 为建，立方为值 创建字典

cubes = {x : x**3 for x in range(1,11)}
print(cubes)

# 生成器推导式
#创建一个生成器，产生 0~9 的平方数，并使用 next() 取出前三个值。
gen = (i ** 2 for i in range(1,10))
print(gen)
