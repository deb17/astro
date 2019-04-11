from concurrent.futures import ThreadPoolExecutor
import re

import requests
import bs4

def astronomy_dot_com():

    domain = 'http://www.astronomy.com'
    try:
        resp = requests.get(domain)
        resp.raise_for_status()
    except Exception:
        url = ('https://via.placeholder.com/600x400?'
               'text=Image+unavailable.+Try+reloading.')
        caption = 'NA'
        news = [('', 'Unavailable. Try reloading the page.')]
        return {'picture-of-the-day': (url, caption), 'news': news}

    html = resp.content

    soup = bs4.BeautifulSoup(html, 'lxml')

    url = ''
    for i in soup.select('.previewImage'):
        if i.a['href'].find('picture-of-day') > -1:
            url = domain + i.img['src']
            url = re.sub(r'\d+$', '600', url)
            caption = i.next_sibling.text
            break

    el = soup.select('.ladderNews')[0]

    news = []
    for i in el.select('.content'):
        news.append((domain + i.div.a['href'], i.div.text))

    return {'picture-of-the-day': (url, caption), 'news': news}

def nasa_apod():

    domain = 'https://apod.nasa.gov/'
    try:
        resp = requests.get(domain)
        resp.raise_for_status()
    except Exception:
        url = ('https://via.placeholder.com/600x400?'
               'text=Image+unavailable.+Try+reloading.')
        caption = 'NA'
        return {'picture-of-the-day': (url, caption), 'news': []}

    html = resp.content

    soup = bs4.BeautifulSoup(html, 'lxml')

    if soup.img:
        url = domain + soup.img['src']
    else:
        url = ('https://via.placeholder.com/600x400?'
               'text=No+image+at+apod.nasa.gov')
        caption = 'No image.'
        return {'picture-of-the-day': (url, caption), 'news': []}

    caption = soup.select('center')[1].b.text

    return {'picture-of-the-day': (url, caption), 'news': []}

def space_dot_com():

    domain = 'https://www.space.com'
    try:
        resp = requests.get(domain)
        resp.raise_for_status()
    except Exception:
        img_url = ('https://via.placeholder.com/600x400?'
                   'text=Image+unavailable.+Try+reloading.')
        url = 'NA'
        news = [('', 'Unavailable. Try reloading the page.')]
        return {'picture-of-the-day': (img_url, url), 'news': news}

    html = resp.content

    soup = bs4.BeautifulSoup(html, 'lxml')

    news = []
    for i in range(1, 6):
        class_ = '.result' + str(i)
        ele = soup.select_one(class_)
        if not ele:
            break
        url = ele.a['href']
        text = ele.select_one('.article-name').text
        news.append((url, text))

    news = [item for item in news if item[1] != 'Image of the Day']

    try:
        image_container = soup.select('[href*="34-image-day"]')[1]
        img_url = image_container.img['data-src']
    except Exception:
        image_container = soup.select_one('#Item1')
        img_url = image_container.img['src']
        url = image_container.a['href']
    else:
        url = image_container['href']

    img_url = re.sub(r'-\d+-\d+.jpg$', '-600-80.jpg', img_url)

    return {'picture-of-the-day': (img_url, url), 'news': news}

def sky_and_telescope():

    domain = 'https://www.skyandtelescope.com'
    try:
        resp = requests.get(domain)
        resp.raise_for_status()
    except Exception:
        news = [('', 'Unavailable. Try reloading the page.')]
        return {'picture-of-the-day': (), 'news': news}

    html = resp.content

    soup = bs4.BeautifulSoup(html, 'lxml')

    ul = None
    for h3 in soup.select('.widget-title'):
        if h3.text == 'Astronomy News':
            ul = h3.next_sibling.next_sibling
            break

    if ul:
        news = []
        for li in ul.select('li')[:5]:
            news.append((li.a['href'], li.a.text.strip()))
    else:
        news = [('', 'Unavailable. Try reloading the page.')]

    return {'picture-of-the-day': (), 'news': news}

def main():

    with ThreadPoolExecutor(max_workers=4) as executor:
        f1 = executor.submit(astronomy_dot_com)
        f2 = executor.submit(nasa_apod)
        f3 = executor.submit(space_dot_com)
        f4 = executor.submit(sky_and_telescope)

        scraped_data_1 = f1.result()
        scraped_data_2 = f2.result()
        scraped_data_3 = f3.result()
        scraped_data_4 = f4.result()

    return (scraped_data_1, scraped_data_2, scraped_data_3, scraped_data_4)
