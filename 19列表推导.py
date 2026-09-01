# 列表推导式 – 字符串列表转大写     words = ['hello', 'world', 'python']，生成全大写的列表。

words = ['hello', 'world', 'python']
upper_words = [w.upper() for w in words]
print(upper_words)  # ['HELLO', 'WORLD', 'PYTHON']
