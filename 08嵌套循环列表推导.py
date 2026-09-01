#将两个列表 [1,2,3] ['a','b'] 中元素配对成元组 且仅保留数字为奇数的组合
list1 = [1,2,3]
list2 = ['a','b']
pairs = [(x,y) for x in list1 for y in list2 if x % 2 != 0]
print(pairs)

# 集合推导 提取字符串中所有不发元音的字母

list = ['c','d','e','f','a','e','h','i']
key = {c for c in list if c in 'aeiou'}
print(key)
