import json
import re
import time
import requests
from bs4 import BeautifulSoup

url = 'https://www.superdrug.com/Make-Up/Nails/Nail-Polish/Gloss-Nail-Polish/Sally-Hansen-Insta-Dri-Nail-Colour---233-Petal-Pusher/p/800437'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}

page = requests.get(url, headers=headers)
time.sleep(5)
soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.contents)

# title_box = soup.find('div', attrs={'class': 'col-sd col-sd--netbook-6 pdp__shortDecPromo'})
title = soup.find('h1', attrs={'class': 'pdp__productName'}).text
print(title)

product_description = soup.find('section', attrs={'class': 'col-sd col-sd--tablet-7 col-sd--netbook-8 col-sd--desktop-9 pdp__details--container'})
sku = product_description.find('p', attrs={'itemprop': 'sku'}).text
print(sku)

pattern = re.compile("'ecommerce': .*?\}\);", re.DOTALL | re.MULTILINE)
details = re.search(pattern, str(soup.contents))

price = re.search("'price': '(.+?)'", str(details.group())).group(1)
print(price)

in_stock = re.search("'in stock': '(.*?)'", str(details.group())).group(1)
print(in_stock)

# 'https://api.bazaarvoice.com/data/batch.json?passkey=i5l22ijc8h1i27z39g9iltwo3&apiversion=5.5&displaycode=10798-en_gb&resource.q0=products&filter.q0=id%3Aeq%3A800055&stats.q0=questions%2Creviews&filteredstats.q0=questions%2Creviews&filter_questions.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_answers.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviews.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&resource.q1=reviews&filter.q1=isratingsonly%3Aeq%3Afalse&filter.q1=productid%3Aeq%3A800055&filter.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&sort.q1=relevancy%3Aa1&stats.q1=reviews&filteredstats.q1=reviews&include.q1=authors%2Cproducts%2Ccomments&filter_reviews.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviewcomments.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_comments.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&limit.q1=10&offset.q1=0&limit_comments.q1=3&callback=bv_351_10687'
