import requests
from lxml import html
import re
import json
import csv


resp = requests.get(url='http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html', headers={
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58'
})

def write_to_json(filename, data):
    with open(filename , 'w') as f:
        f.write(json.dumps(data))

def write_to_csv(filename, data):
    headers = ['title', 'price', 'availability', 'in_stock', 'Warning_text', 'description']
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f,headers)
        writer.writeheader()
        writer.writerow(data)



tree = html.fromstring(html=resp.text)
main_product = tree.xpath("//div[@class='col-sm-6 product_main']")[0]


title = main_product.xpath(".//h1/text()")[0]
price = main_product.xpath(".//p[1]/text()")[0]
availability = main_product.xpath(".//p[2]/text()")[1]
in_stock = re.compile(r'\d+').findall(availability)[0]
Warning_text = tree.xpath("//div[@role='alert']/text()")[0]
description = tree.xpath("//div[@id='product_description']/following-sibling::p/text()")

book_information = {
    'title': title,
    'price': price,
    'availability': in_stock,
    'Warning_text': Warning_text,
    'description': description

}

print(book_information)
write_to_json('book.json', book_information)

write_to_csv('book.csv', book_information)
