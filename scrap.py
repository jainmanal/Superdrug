import json
import re
import time
import traceback

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}


def scrap_data(url):
    try:
        page = requests.get(url, headers=headers)
        time.sleep(5)
        soup = BeautifulSoup(page.text, 'html.parser')
        # print(soup.contents)

        pattern = re.compile("'ecommerce': .*?\}\);", re.DOTALL | re.MULTILINE)
        details = re.search(pattern, str(soup.contents))
        print(details.group())

        # title_box = soup.find('div', attrs={'class': 'col-sd col-sd--netbook-6 pdp__shortDecPromo'})
        title = soup.find('h1', attrs={'class': 'pdp__productName'}).text
        print('Product Name: ' + title)

        # sku = product_description.find('p', attrs={'itemprop': 'sku'}).text
        sku = re.search("'id': '(.+?)'", str(details.group())).group(1)
        print('SKU: ' + sku)

        price = re.search("'price': '(.+?)'", str(details.group())).group(1)
        print('Price: ' + price)

        in_stock = re.search("'in stock': '(.*?)'", str(details.group())).group(1)
        print('Available: ' + in_stock)

        product_url = re.search("'url': '(.*?)'", str(details.group())).group(1)
        print('Product Url: ' + product_url)

        try:
            product_description = soup.find('div', attrs={'id': 'pdp__details'})

            try:
                product_info = product_description.find('p', attrs={'itemprop': 'description'}).text
                print('Product Info: ' + product_info)
            except:
                print('Product Info: Not Available')

            try:
                product_specification = product_description.find(text='Product Specification').findNext('p').contents[0]
                print('Product Specification: ' + product_specification)
            except:
                print('Product Specification: Not Available')
        except:
            print('Description Error')
            pass

        try:
            image_box = soup.find('a', attrs={'class': 'pdp-gallery__main-img'})
            image_url = image_box.find('img').get('src')
            print('Image Url: ' + image_url)
        except:
            print("Image Url: Not Available")

        try:
            breadcrumb = soup.find('div', attrs={'id': 'breadcrumb'}).text
            print('Breadcrumbs: ' + breadcrumb)
        except:
            pass

        reviews_url = f'https://api.bazaarvoice.com/data/batch.json?passkey=i5l22ijc8h1i27z39g9iltwo3&apiversion=5.5&displaycode=10798-en_gb&resource.q0=products&filter.q0=id%3Aeq%3A{sku}&stats.q0=questions%2Creviews&filteredstats.q0=questions%2Creviews&filter_questions.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_answers.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviews.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&resource.q1=reviews&filter.q1=isratingsonly%3Aeq%3Afalse&filter.q1=productid%3Aeq%3A{sku}&filter.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&sort.q1=relevancy%3Aa1&stats.q1=reviews&filteredstats.q1=reviews&include.q1=authors%2Cproducts%2Ccomments&filter_reviews.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviewcomments.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_comments.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&limit.q1=10&offset.q1=0&limit_comments.q1=3&callback=bv_351_10687'
        reviews_text = requests.get(reviews_url, headers=headers).text
        reviews = re.search(r'\((.*?)\)$', reviews_text).group(1)
        reviews_json = json.loads(str(reviews))
        print('Reviews JSON:', reviews_json)

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(e)


url = 'https://www.superdrug.com/Skin/Body-Care/Dry-Skin/CeraVe-Hydrating-Cream-to-Foam-Cleanser-236ml/p/783507'
scrap_data(url)
