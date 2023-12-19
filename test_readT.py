from readability import Document
import requests

url = "https://twitter.com/dotey/status/1736980589117411788"

from phantomjs import Phantom

phantom = Phantom()

conf = {
    'url': url,   # Mandatory field
    'output_type': 'html',          # json for json
    'min_wait': 1000,               # 1 second
    'max_wait': 30000,              # 30 seconds
    'selector': '',                 # CSS selector if there's any
    'resource_timeout': 3000,       # 3 seconds
    'headers': {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.72 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Sec-Fetch-Mode": "navigate",
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
    },
    'cookies': [
        
    ],
    'functions': [
        'function(){window.location.replace("'+ url +'");}',
    ],
}


output = phantom.download_page(conf)


print ( output )
'''
doc = Document(response.text)

print(doc.title())     # 标题
print(doc.summary())   # 主体内容
'''