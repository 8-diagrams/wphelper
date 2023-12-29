from goose3 import Goose
from goose3.text import StopWordsChinese
url  = 'https://blog.csdn.net/bit_clearoff/article/details/52502654'
g = Goose({'stopwords_class': StopWordsChinese, 'browser_user_agent': 'Mozilla'})
article = g.extract(url=url)
print ( article._links )
print( article._cleaned_text )
print (article.cleaned_text[:150])
