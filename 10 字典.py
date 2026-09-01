# 创建一个空字典，然后依次添加 'name': 'chh'、'age': 23、'city': 'HeFei'。

info = {}
info["name"] = "chh"
info["age"] = 23
info["city"] = "HeFei"
print(info)


#合并两个字典
dict1 = {'你好','再见'}
dict2 = {'吃饭','睡觉'}
dict1.update(dict2)
print(dict1)

#删除字典中的键 从字典 {'x': 10, 'y': 20, 'z': 30} 中删除键 'y'
d = {'x': 10, 'y': 20, 'z': 30}
del d['y']
print(d)
