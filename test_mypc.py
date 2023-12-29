from readability import Document
import requests

url = "https://blog.csdn.net/mouday/article/details/94021769"
response = requests.get(url)
#response.encoding = "utf-8"

doc = Document(response.text)

print ( doc )
print(doc.title())     # 标题
print(doc.summary())   # 主体内容

