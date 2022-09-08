from os import link
from turtle import title
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
#format the file
clear = open('articles.csv', 'w+')
clear.close
#here we add links to substacks archives, only articles (no podcasts)
url_list = ['https://nosleep.substack.com/archive', 'https://onchainwizard.substack.com/archive', 'https://cobie.substack.com/archive', 'https://thedailydegen.substack.com/archive']
for url in url_list:
    response = requests.get(url)
    #We convert the response into unicode for standardization purposes
    text = response.text
    html_data = BeautifulSoup(text, 'html.parser')
    #Define the columns
    header = ["Titles", "Links", "Author"]
    titles_together = ''
    links_together = ''
    #extracting the data we wish to store
    for a in html_data.find_all('a', class_="post-preview-title newsletter"):
        titles_together += str(a.contents)
        titles_together += ' '
        links_together += str(a['href'])
        links_together += ' '
    author = html_data.find('a', class_="navbar-title-link").contents
    #formatting the titles
    for bracket in titles_together:
        titles_together = titles_together.replace('[','')
    #separating each title and link into individuals
    titles = titles_together.split("] ")
    links = links_together.split(" ")
    authors = [None]*(len(titles)-1)
    for index in range(len(titles) - 1):
        authors[index] = author
    final_news = []
    if len(titles) == len(links):
        final_news = list(zip(titles, links, authors))
    else:
        raise Exception('Missing titles or links')
    #write the data into the file
    with open("articles.csv", 'a', encoding="utf-8", newline='') as open_file:
        writer = csv.writer(open_file)
        writer.writerows(final_news)
        open_file.close()
