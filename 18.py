# 非递归
n = 4
sum = 1
for i in range(1, n + 1):
    sum *= i
print(sum)

# 递归
def jie_cheng(num):
    if num == 1:
        return 1
    else:
        return num * jie_cheng(num - 1)
print(jie_cheng(4))