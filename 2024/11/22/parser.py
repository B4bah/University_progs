import requests
from bs4 import BeautifulSoup

url = 'https://www.smtu.ru/ru/viewschedule/20150/'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

tutors = set()
for item in soup.findAll('small'):
    if len(item.text.split()) == 3:
        tutors.add(item.text)

for item in tutors:
    print(item)