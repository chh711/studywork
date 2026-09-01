# 生成1 到 10 的平方列数
from unittest import result

key = [i ** 2 for i in range(1,11)]
print(key)

# 从1-30 选出所有能被 2 整除的偶数
result = [x for x in range(1,31) if x % 2 == 0]
print(result)
