#  清理字符串 " hello world " 两端的空白字符。
from email import message

s = " Hello World     "
clean = s.strip()
print(clean)

# 字符串格式化（f-string）有变量 name = "czy" 和 age = 22，用 f-string 输出 "My name is czy and I am 22 years old."
name = "czy"
age = 22
message = f"My name is {name} and I am {age} years old"
print(message)

