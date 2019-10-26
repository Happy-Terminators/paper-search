import sys
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd

def get_citations(content):
    end = content.find('회 인용')
    start = 0

    for s in range(end-6, end):
        if content[s] == '>':
            start = s
            break

    return int(content[start + 1 : end])

def get_year(content):
    for char in range(0,len(content)):
        if content[char] == '-':
            out = content[char-5:char-1]
    if not out.isdigit():
        out = 0
    return int(out)

keyword ='starcraft'
start_year = 2017
end_year = 2019

url = 'https://scholar.google.co.kr/scholar?start='+ str(0) +'&q='+ keyword +'&hl=ko&as_sdt=0,5&as_ylo='+str(start_year)+'&as_yhi='+str(end_year)
html = requests.get(url).text

soup = BeautifulSoup(html,  "html.parser")
mydivs = soup.find_all("div", class_="gs_ri")

#print(mydivs[0])
print(get_citations(str(mydivs[1])))
print(get_year(str(mydivs[1].find_all("div", class_="gs_a"))))

try:
    print(mydivs[1].find('h3').find('a').get('href'))
except: # catch *all* exceptions
    print('Look manually at: https://scholar.google.com/scholar?start='+str(n)+'&q=non+intrusive+load+monitoring')
        
try:
    print(mydivs[1].find('h3').find('a').text)
except: 
    print('Could not catch title')

'''
for n in range(0, number_of_results, 10):    
    url = 'https://scholar.google.com/scholar?start='+str(n)+'&q='+keyword.replace(' ','+')
    page = session.get(url)
    c = page.content
    
    # Create parser
    soup = BeautifulSoup(c, 'html.parser')
    
    # Get stuff
    mydivs = soup.findAll("div", { "class" : "gs_r" })
    print(mydivs[0])
 
    for div in mydivs:
        try:
            links.append(div.find('h3').find('a').get('href'))
        except: # catch *all* exceptions
            links.append('Look manually at: https://scholar.google.com/scholar?start='+str(n)+'&q=non+intrusive+load+monitoring')
        
        try:
            title.append(div.find('h3').find('a').text)
        except: 
            title.append('Could not catch title')
            
        citations.append(get_citations(str(div.format_string)))
        year.append(get_year(div.find('div',{'class' : 'gs_a'}).text))
        author.append(get_author(div.find('div',{'class' : 'gs_a'}).text))
'''
