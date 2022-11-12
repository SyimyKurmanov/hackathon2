from bs4 import BeautifulSoup
import csv
import requests

count = 0

def get_html(url: str) ->str:
    response = requests.get(url)
    return response.text

def get_data(html: str) -> bool:

    soup = BeautifulSoup(html, 'html.parser')

    catalog = soup.find('div', class_='listing search-page x-3')
    if not catalog:
        return False

    cars = catalog.find_all('div', class_ = 'listing-item main')
    for car in cars:
        info_link = BeautifulSoup(get_html("https://www.mashina.kg"+car.find('a').get('href')), 'html.parser')
        # print(info_link)
        title = car.find('span', class_='white font-big').text.strip()
        chrs = info_link.find('div', class_='content info').text.strip()
        if not chrs:
            chrs = 'Нет характеристики!'
        # print (chrs)
        price = car.find('span', class_='white custom-margins font-small')
        if price is not None:
            price = price.text
        else:
            price = car.find('span', class_='white custom-margins font-big').text
        try:   
            image = car.find('div', class_="main-image").find('img').get('data-src')
        except:
            image= 'Нет картинки!'
        print(image)
        data = {
            'title': title,
            'chrs': chrs,
            'price': price,
            'img': image
        }
        write_to_csv(data)
    return True

def write_to_csv(data: dict)-> None:
    global count
    with open('automobiles.csv', 'a') as file:
        fieldnames = ['№','Название', 'Характеристика', 'Цена', 'Фото']
        writer = csv.DictWriter(file, fieldnames)
        count += 1
        writer.writerow({
            '№': count,
            'Название': data.get('title'),
            'Характеристика': data.get('chrs'),
            'Цена': data.get('price'),
            'Фото': data.get('img')
        })

def prepare_csv():
    with open('automobiles.csv', 'w') as file:
        fieldnames = ['№', 'Название', 'Характеристика', 'Цена', 'Фото']
        writer = csv.DictWriter(file, fieldnames)   
        writer.writerow({
            '№': '№',
            'Название': 'Название',
            'Характеристика': 'Характеристика',
            'Цена': 'Цена',
            'Фото': 'Фото' 
        })

def main():
    i = 1
    prepare_csv()
    while True:
        BASE_URL = f'https://www.mashina.kg/new/search?page={i}'
        html = get_html(BASE_URL)
        is_res = get_data(html)
        if not is_res:
            break
        print(f'Страница {i}')
        i += 1

main()