import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://cobie.substack.com/archive?sort=new'
response = requests.get(url)
#We convert the response into unicode for standardization purposes
text = response.text
html_data = BeautifulSoup(text, 'html.parser')

for a in html_data.find_all('a', class_="post-preview-title newsletter"):
    print(a[])
    print(a['href'])