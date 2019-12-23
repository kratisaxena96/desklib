import os
from bs4 import BeautifulSoup
import requests
# exec(open("./scapping-subjects-data.py").read())

url = "https://www.ukessays.com/services/example-essays/"
source = requests.get(url)

soup = BeautifulSoup(source.text, 'html')

title = soup.find('title')
path = os.getcwd()
if not os.path.exists('scrapping'):
    os.mkdir("scrapping")
for tag in soup.find_all(id="category-list"):
    rows = tag.find_all('a')
    for a in rows:
        path_str = a['href'].replace('/',' ')
        first_directory = os.path.join(path,"scrapping",path_str)
        if not os.path.exists(first_directory):
            os.mkdir(first_directory)
        source_first = requests.get(url+"/%s"%(a['href']))
        int_soup = BeautifulSoup(source_first.text, 'html')
        for anchor in int_soup.find_all("ul", {"class": "e-category-list"}):
            anc = anchor.find_all('a')
            for val in anc:
                source_second = requests.get(url+"/%s/%s"%(a['href'],val['href']))
                int_soup_first = BeautifulSoup(source_second.text, 'html')
                qwery_text = int_soup_first.find_all("div", {"class": "content"})
                completeName = os.path.join(first_directory, "%s"%(val['href']) + ".txt")
                with open(completeName, 'w') as f:
                    data = qwery_text[0].text
                    f.write(data)

