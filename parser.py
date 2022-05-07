import requests
from bs4 import BeautifulSoup
import lxml
import re
import psycopg2

req = requests.get("https://monitoring.meteo.uz/uz/map/view/107").text
soup = BeautifulSoup(req, 'lxml')


# MAIN INFO BAR
info_bar = soup.find('div', class_= 'col-xl-12')
view = info_bar.find('div', class_= 'view-item')
# print(" #"*99)


title_bar = view.find('div', 'view-item__title')
title = title_bar.find('h2').text
# print(title)
# print("# "*99)


date = info_bar.find('p').text

# DATE CONVERSION

p_sana_vaqt  = r'\d{2}\.\d{2}\.\d{4}, ?\d{2}\:\d{2}'
from datetime import datetime
date = re.findall(p_sana_vaqt, date)
date = date[0]
date = datetime.strptime(date, '%d.%m.%Y, %H:%M')
date.strftime('%Y-%m-%d %H:%M')

print(date)
print("# "*99)


# TAKING MAIN INFORMATION
infos = info_bar.find_all('span', class_='vi-nopart')

titles = []
datas = []
info_dict = {}

for index, data in enumerate(infos):
    if index % 2 == 0:
        titles.append(data)
    else:
        datas.append(data)

for title, data in zip(titles, datas):
    title = title.text
    data = data.text
    info_dict[title] = data

date = f'{date}'
info_dict['date'] = date
print(info_dict)
