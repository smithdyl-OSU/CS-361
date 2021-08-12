import requests
import json
from bs4 import BeautifulSoup


article = requests.get('https://en.wikipedia.org/wiki/Special:Random').text
soup = BeautifulSoup(article, 'html.parser')
h1 = soup.find('h1', id='firstHeading')
h1 = h1.string
data = h1.replace(' ', '_')
response = requests.get('http://flip2.engr.oregonstate.edu:8797/?u=' + data)
inspiration = response.json()['title'][0]
print(inspiration)