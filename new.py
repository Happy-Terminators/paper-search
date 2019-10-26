import sys
import requests
from bs4 import BeautifulSoup

def get_citations(content):
    out = 0
    for char in range(0,len(content)):
        if content[char:char+5] == '회 인용':
            init = char                      
            for end in range(init-6, init):
                if content[end] == '>':
                    break
            out = content[end+1:init]
            print(out)
    return int(out)
    
def get_year(content):
    for char in range(0,len(content)):
        if content[char] == '-':
            out = content[char-5:char-1]
    if not out.isdigit():
        out = 0
    return int(out)

def get_author(content):
    for char in range(0,len(content)):
        if content[char] == '-':
            out = content[2:char-1]
            break
    return out

keyword = 'starcraft'
url = 'https://scholar.google.com/scholar?start='+str(1)+'&q='+keyword.replace(' ','+')
html = requests.get(url).text

soup = BeautifulSoup(html,"html5lib")
mydivs = soup.findAll("div", { "class" : "gs_r" })
#print(mydivs[0])

for div in mydivs:
    
    try:
        print(div.find('h3').find('a').get('href'))
    except: # catch *all* exceptions
        print('Look manually at: https://scholar.google.com/scholar?start='+str(1)+'&q=non+intrusive+load+monitoring')
       
    try:
        print(div.find('h3').find('a').text)
    except: 
        print('Could not catch title')

    print(get_citations(str(div.format_string)))
    print(get_year(div.find('div',{'class' : 'gs_a'}).text))
    print(get_author(div.find('div',{'class' : 'gs_a'}).text))
    print()
