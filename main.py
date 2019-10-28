import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

keyword ='starcraft'
start_year = 2017
end_year = 2019
total_paper = 10000
total_page = 1000
maximum_paper = 20

basic_dir = os.getcwd()

min_cit = 0
is_page_avaliable = True
first_page_n = 0

title = ""
links = ""
citation = 0
year = 0
source = list()

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


def extract(html, is_text, maximum_n, data, min_citation):
    soup = BeautifulSoup(html, "html5lib")
    papers = soup.find_all("div", class_="gs_ri")

    if papers:
        for paper in papers:

            citation = (get_citations(str(paper)))

            if data.shape[0] < maximum_paper:
                try:
                    title = (paper.find('h3').find('a').text)
                except: 
                    title = ('Could not catch title')

                try:
                    links = (paper.find('h3').find('a').get('href'))
                except: # catch *all* exceptions
                    links = ('Look manually at: https://scholar.google.co.kr/scholar?start='+ str(page_n * 10) +'&q='+ keyword +'&as_ylo='+str(start_year)+'&as_yhi='+str(end_year))
            
                year = (get_year(str(paper.find_all("div", class_="gs_a"))))

                data = data.append({'Title': title, 'Link': links, 'Citations': citation, 'Year': year}, ignore_index=True)
                data = data.sort_values('Citations', ascending=False)
                data = data.reset_index(drop=True)
                min_citation = data.loc[data.shape[0]-1, 'Citations']

            elif citation > min_citation:
                try:
                    title = (paper.find('h3').find('a').text)
                except: 
                    title = ('Could not catch title')

                try:
                    links = (paper.find('h3').find('a').get('href'))
                except: # catch *all* exceptions
                    links = ('Look manually at: https://scholar.google.co.kr/scholar?start='+ str(page_n * 10) +'&q='+ keyword +'&as_ylo='+str(start_year)+'&as_yhi='+str(end_year))
            
                year = (get_year(str(paper.find_all("div", class_="gs_a"))))

                data = data.append({'Title': title, 'Link': links, 'Citations': citation, 'Year': year}, ignore_index=True)
                data = data.sort_values('Citations', ascending=False)
                data = data.reset_index(drop=True)
                data = data.drop(maximum_paper)

                min_citation = data.loc[maximum_paper-1, 'Citations']

        if is_text:
            source.append(str(page_n) + "~" + str((page_n + 1)* 10 - 1) + " : txt")
            return data, min_citation, True
        else:
            source.append(str(page_n) + "~" + str((page_n + 1)* 10 - 1) + " : internet")
            return data, min_citation, True
    else:
        source.append(str(page_n) + "~" + str((page_n + 1)* 10 - 1) + " : manual")
        return data, min_citation, False

result_data = pd.DataFrame(columns=['Title', 'Link', 'Citations', 'Year'])
csv_dir = basic_dir + "\\" +keyword + "\\" +keyword + ".csv"
info_dir = basic_dir + "\\" +keyword + "\\info.txt"

if os.path.isfile(csv_dir):
    result_data = pd.read_csv(csv_dir)

last_page = 0

for page_n in range(first_page_n, 3):
    
    html_dir = basic_dir + "\\" +keyword +"\\htmls\\page" + str(page_n) + ".txt"

    if os.path.isfile(html_dir):
        f = open(html_dir, 'r')
        html = f.read()
        f.close()

        if is_page_avaliable:
            result_data, min_cit, is_page_avaliable = extract(html, True, maximum_paper, result_data, min_cit)
        else:
            last_page = page_n
            break
    else:
        url = 'https://scholar.google.co.kr/scholar?start='+ str(page_n * 10) +'&q='+ keyword +'&as_ylo='+str(start_year)+'&as_yhi='+str(end_year)
        html = requests.get(url).text

        f = open(html_dir, 'w')
        f.write(html)
        f.close()

        if is_page_avaliable:
            result_data, min_cit, is_page_avaliable = extract(html, True, maximum_paper, result_data, min_cit)
        else:
            last_page = page_n
            break

        rand_value = random.randint(1, 10)
        time.sleep(rand_value)


result_data.to_csv(csv_dir, encoding='utf-8')

f = open(info_dir, 'w')
f.write("This table searched " +str(last_page * 10)+" pages\n")
for info in source:
    f.write(info+"\n")
f.close()


print(source)
