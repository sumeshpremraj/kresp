import re
import requests
from bs4 import BeautifulSoup

genre = 'art';

s = requests.Session()
link = 'https://www.goodreads.com/genres/'+ genre
r = s.get(link)

def getRating(x):
    st = str(x.parent.findChildren(text=re.compile("CDATA")))
    if "avg rating" in st:
        return st[0:st.find("avg")][-5:-1]

soup = BeautifulSoup(r.text, "html5lib")
print (soup.html.title.text)
tmp = []
for x in soup.find_all(class_='coverWrapper'):
    tmp.append({
        'bookTitle': x.img['alt'],
        'link': 'https://www.goodreads.com' + x.a['href'],
        'rating': getRating(x)
        })
sorted_list = sorted(tmp, key=lambda k: float(k['rating']), reverse = True)
print (sorted_list)    
