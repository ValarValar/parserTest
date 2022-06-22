import os
import xml.etree.ElementTree as ET
from datetime import datetime
from itertools import islice, chain
from alive_progress import alive_bar

import requests

SOURCE_URL = "http://stripmag.ru/datafeed/p5s_full_stock.xml"
TARGET_URL = "http://alitair.1gb.ru/Intim_Ali_allfids_2.xml"
DATA_PATH = "feed_update_data/"
DATA_DIR = "feed_update_data"
CHUNK_SIZE = 50


def getter_name_with_ext_from_url(url):
    return os.path.basename(url)


def getter_now_time():
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


def data_dir_check_or_create(DIR=DATA_DIR):
    if not os.path.isdir(DIR):
        os.mkdir(DIR)


def download_file_from_url(url):
    data_dir_check_or_create()
    file = DATA_PATH + getter_name_with_ext_from_url(url)

    response = requests.get(url)
    with open(file, 'wb') as f_out:
        f_out.write(response.content)
    print(f'{getter_now_time()}: {file} successfully downloaded')
    return file


def chunks(iterable, size=CHUNK_SIZE):
    iterator = iter(iterable)
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))


def update_feed(source, target):
    # Get Tree of source file
    source_tree = ET.parse(source)
    source_root = source_tree.getroot()
    source_products = source_root.iter('product')

    target_tree = ET.parse(target)
    target_root = target_tree.getroot()
    target_offers = target_root.find('shop').find('offers')

    cnt = 1
    print(f'Processing ({CHUNK_SIZE} elems) chunks...')
    with alive_bar(0) as bar1:
        for chunk in chunks(source_products):
            elem_list = list(chunk)
            cnt += 1
            for source_elem in elem_list:
                source_id = source_elem.get('prodID')
                target_offer = target_offers.find(f'offer[@id="{source_id}"]')
                if target_offer is None:
                    continue
                source_price = source_elem.find('price')
                source_count = source_elem.find('assortiment').find('assort')

                target_price = target_offer.find('price')
                target_count = target_offer.find('quantity')

                # Change quantity
                target_count.text = source_count.get('sklad')

                # Change prices
                target_price.set('BaseRetailPrice', source_price.get('BaseRetailPrice'))
                target_price.set('BaseWholePrice', source_price.get('BaseWholePrice'))
                target_price.set('RetailPrice', source_price.get('RetailPrice'))
                target_price.set('WholePrice', source_price.get('WholePrice'))
            bar1()

    print(f'{getter_now_time()}: {cnt - 1} chunk successfully processed')
    target_tree.write(target, encoding="utf-8")
    print(f'{getter_now_time()}: updated file is {target}')


if __name__ == "__main__":
    source_file = download_file_from_url(SOURCE_URL)
    target_file = download_file_from_url(TARGET_URL)

    update_feed(source_file, target_file)
