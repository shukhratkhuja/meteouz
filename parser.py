import requests
from bs4 import BeautifulSoup
import re
from dbconnector import cconn, cursor

URL = "https://monitoring.meteo.uz/uz/map/view/107"

def date_formatter(date_raw):
    p_sana_vaqt  = r'\d{2}\.\d{2}\.\d{4}, ?\d{2}\:\d{2}'
    from datetime import datetime
    date = re.findall(p_sana_vaqt, date_raw)
    date = date[0]
    new_date = datetime.strptime(date, '%d.%m.%Y, %H:%M')
    new_date.strftime('%Y-%m-%d %H:%M')
    return new_date

def scraper(req):
    
    soup = BeautifulSoup(req.text, 'html.parser')

    # MAIN INFO BAR
    info_bar = soup.find('div', class_= 'col-xl-12')
    view = info_bar.find('div', class_= 'view-item')
    # print(" #"*99)

    title_bar = view.find('div', 'view-item__title')
    title = title_bar.find('h2').text
    # print(title)
    # print("# "*99)

    date_raw = info_bar.find('p').text
    
    # DATE CONVERSION
    date = date_formatter(date_raw)

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
    info_dict['date'] = date
    return info_dict

def db_insertion(info):
    # TABLE CREATION
    query_table_creation = """CREATE TABLE IF NOT EXISTS uzgidromet.pollutant_consentrations 
                            (azot_oksidi VARCHAR(20), 
                            amiak VARCHAR(20), 
                            azon VARCHAR(20), 
                            oltingugurt_dioksidi VARCHAR(20), 
                            azot_dioksidi VARCHAR(20), 
                            uglerod_oksidi VARCHAR(20),
                            pm2_5 VARCHAR(20),
                            pm10 VARCHAR(20), 
                            date TIMESTAMP)
                            """

    cursor.execute(query_table_creation)

    # DATA INSERTION

    query_data_insertion = """INSERT INTO uzgidromet.pollutant_consentrations
                            VALUES 
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """


    insertion_values = tuple(info.values())
    print(insertion_values)
    cursor.execute(query_data_insertion, insertion_values)


def main():
    try:
        req = requests.get(URL)
        info = scraper(req)
        db_insertion(info)

    except ConnectionError: 
        print("Error with Connection !")
    except Exception as e:
        print("Error: ", e)
    finally:
        cconn.close()


main()

