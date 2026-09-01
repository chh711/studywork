#遍历字典 – 打印所有键值 遍历字典 {'name': 'czy', 'age': 22, 'job': ' AI engineer'}，按 key: value 格式打印
from pip._internal.index import sources

d = {'name': 'czy', 'age': 22, 'job': ' AI engineer'}
for k, v in d.items():
    print(f'{k}: {v}')

#  按值排序字典（返回排序后的键列表） scores = {'A': 88, 'B': 75, 'C': 92, 'D':95}，按分数从高到低输出学生姓名
sources = {'A': 88, 'B': 75, 'C': 92, 'D': 95}
sorted_names = sorted(sources,key=sources.get,reverse=True)
print(sorted_names)

#使用 get() 安全访问不存在的键：从字典 {'a': 1, 'b': 2} 中获取键 'c'，若不存在则返回默认值 0
d = {'a':1,'b':2}
val = d.get('c')
print(val)
