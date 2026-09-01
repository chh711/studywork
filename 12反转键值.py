#字典推导式 – 反转键值  给定 {'a': 1, 'b': 2, 'c': 3}，生成新字典 {1: 'a', 2: 'b', 3: 'c'}（假设值唯一）
from tomlkit import table

d = {'chh':1,'czy':2,'lrh':3}
reversed_d = {v:k for k,v in d.items()}
print(reversed_d)

