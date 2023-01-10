from os import link
from turtle import title
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from config import url_list
title_count = 0
link_count = 0
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

    #scrapping for substacks
    if 'archive' in url:    
        #Getting all the articles' titles
        for a in html_data.find_all('a', class_="post-preview-title newsletter"):
            titles_together += str(a.contents)
            titles_together += ' '
            #Getting all the articles' links
            links_together += str(a['href'])
            links_together += ' '
            title_count += 1
            link_count += 1
        #Getting the author    
        author = html_data.find('a', class_="navbar-title-link").contents
        #Getting the date of publication
        for time in html_data.find_all('time'):
            dates_together += str(time.contents)
            dates_together += ' '
    
    #scrapping for mirror articles    
    if 'mirror.xyz' in url:
        #Getting all the articles' links
        for href_a in html_data.find_all('a', class_='_1sjywpl0 _1sjywplf bc5nci1gs bc5nci6t bc5nci50x bc5nci510 bc5nci512 bc5nci519 bc5nci4pq bc5nciih bc5ncijq bc5ncitb bc5nci37k bc5nci451 bc5nci58j bc5nci4sv bc5nci4t0'):
            links_together += str(href_a['href'])
            links_together += ' '
            link_count += 1
        #Getting all the articles' titles
        for a in html_data.find_all(class_="_1sjywpl0 bc5nci53h bc5nci4s8 bc5ncivy bc5ncivf bc5nciws bc5nci1ou bc5nci1po bc5nci4ta"):
            titles_together += str(a.contents)
            titles_together += ' '
            title_count += 1
        #fixes formatting if some article has no title
        if title_count != link_count:
            while title_count < link_count:
                titles_together += '[Title Missing] '
                title_count += 1
        #Getting the author
        author = html_data.find(class_="_1sjywpl0 _1sjywpl1 bc5nci3lg bc5nci3rz").contents
        #Getting the date of publication
        for time in html_data.find_all(class_="_1sjywpl0 _1sjywpl1 bc5nci3lg bc5nci3rz"):
                dates_together += " 'no date found "
    
    #scrapping for medium articles        
    if 'medium.com' in url:
        print('medium article found')
        #Getting all the articles' links
        for href_a in html_data.find_all('a', class_='ae af ag ah ai aj ak al am an ao ap aq ar as'):
            links_together += href_a['href']
            links_together += ' '
            link_count += 1
        #Getting all the articles' titles
        for a in html_data.find_all(class_="bd jd je dn jf jg gu jh dp ji jj gy jk jl jm jn hc jo jp jq jr hg js jt ju jv hk hl hm hn hp hr bi"):
            titles_together += str(a.contents)
            titles_together += ' '
            title_count += 1
        #fixes formatting if some article has no title
        if title_count != link_count:
            while title_count < link_count:
                titles_together += '[Title Missing] '
                title_count += 1
        #Getting the author
        author = html_data.find('a', class_="ae af ag ah ai aj ak al am an ao ap aq ar as").contents
        #Getting the date of publication
        for time in html_data.find_all(class_="bd b be z dk"):
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
    final_news = list(zip(titles, links, authors, dates))
    with open("articles.csv", 'a', encoding="utf-8", newline='') as open_file:
        writer = csv.writer(open_file)
        writer.writerow(space)
        writer.writerow(header)
        writer.writerows(final_news)
        open_file.close()

