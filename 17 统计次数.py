#统计字符串中每个字符出现次数（使用字典）

s = "adcdefghiugk"
counts = {}
for ch in s:
    counts[ch] = counts.get(ch, 0) + 1
print(counts)  # {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}