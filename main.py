from os import link
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv


url = 'https://nosleep.substack.com/archive'
response = requests.get(url)
#We convert the response into unicode for standardization purposes
text = response.text
html_data = BeautifulSoup(text, 'html.parser')
header = ['Titles', 'Links']
titles_together = ''
links_together = ''

for a in html_data.find_all('a', class_="post-preview-title newsletter"):
    titles_together += str(a.contents)
    titles_together += ' '
    links_together += str(a['href'])
    links_together += ' '

titles = titles_together.split("] ")
links = links_together.split(" ")
with open(r"C:\Users\34619\OneDrive\Desktop\web3 data\news bot\News-Bot\articles.csv", 'w') as open_file:
    writer = csv.writer(open_file)
    writer.writerow(titles)
    writer.writerow(links)
    open_file.close()
print(links)
print(titles)