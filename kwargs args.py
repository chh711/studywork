def eat_fruits(*args):
    print(f"收到的水果有：{args}")  # args 是一个元组
    for fruit in args:
        print(f"- {fruit}")

# 调用
eat_fruits("苹果", "香蕉", "橘子")


def show_info(**kwargs):
    print(f"收到的信息有：{kwargs}")  # kwargs 是一个字典
    for key, value in kwargs.items():
        print(f"{key} = {value}")

# 调用
show_info(name="czy", age=22, city="合肥")


def complex_func(a, b, *args, c=100, **kwargs):
    print(f"a={a}, b={b}")          # 必填位置参数
    print(f"args={args}")           # 多余的位置参数
    print(f"c={c}")                 # 默认参数
    print(f"kwargs={kwargs}")       # 多余的关键字参数

# 调用测试
complex_func(1, 2, 3, 4, 5, c=200, name="chh", age=22)