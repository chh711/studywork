# 1，2，3，4，5，6，7，8，9，10
# 递归
def fib(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)
print(fib(5))

# 非递归
n = 6
fibs = [1,1]
for i in range(2,n+1):
    fibs.append(fibs[i-1] + fibs[i-2])
print(n - 1)
