from os import link
from turtle import title
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from config import url_list
#format the file
clear = open('articles.csv', 'w+')
clear.close
#here we add links to substacks archives, only articles (no podcasts)
for url in url_list:
    response = requests.get(url)
    #We convert the response into unicode for standardization purposes
    text = response.text
    html_data = BeautifulSoup(text, 'html.parser')
    #Define the columns
    header = ["Titles", "Links", "Author", "Date"]
    space = [" ", " ", " ", " "]
    titles_together = ''
    links_together = ''
    dates_together = ''
    #extracting the data we wish to store
    for a in html_data.find_all('a', class_="post-preview-title newsletter"):
        titles_together += str(a.contents)
        titles_together += ' '
        links_together += str(a['href'])
        links_together += ' '
    author = html_data.find('a', class_="navbar-title-link").contents
    for time in html_data.find_all('time'):
        dates_together += str(time.contents)
        dates_together += ' '
    #formatting the entries
    for bracket in titles_together:
        titles_together = titles_together.replace('[','')
        dates_together = dates_together.replace('[','')
        dates_together = dates_together.replace(']','')
    #separating each title and link into individuals
    titles = titles_together.split("] ")
    links = links_together.split(" ")
    dates = dates_together.split(" '")
    authors = [None]*(len(titles)-1)
    for index in range(len(titles) - 1):
        authors[index] = author
    final_news = []
    if len(titles) == len(links):
        final_news = list(zip(titles, links, authors, dates))
    else:
        raise Exception('Missing titles or links')
    #write the data into the file
    with open("articles.csv", 'a', encoding="utf-8", newline='') as open_file:
        writer = csv.writer(open_file)
        writer.writerow(space)
        writer.writerow(header)
        writer.writerows(final_news)
        open_file.close()

