# !pip install aiohttp
# !pip install aiofiles
# dbutils.library.restartPython()


import sys
# sys.path.insert(0, './Scripts')

import pandas as pd
import numpy as np
import os
import json
# import utility as u
# import scrape_to_embedding as stem
from datetime import datetime
# import image_embedding_script as ies
import time
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import ElementNotInteractableException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys


def json_to_df(data):
        '''
        myntra api data in json convert to dataframe
        path = files path
        files : files = [x for x in os.listdir('/content/data/myntra')]
        return pandas Dataframe
        '''
        main_data = pd.DataFrame()

        # files = [x for x in os.listdir(path)]
        # print(f'number of files {len(files)}')

        # for index1,pid in enumerate(files):
        #     if index1 % 100 == 0:
        #         print(f'file number {index1+1}')
        #     # print(f'page start {pid}')
        #     file_path = os.path.join(path,pid)
        #     data = self.file_open(file_path)
        # #   df.loc[index,'doc_id'] = pid.strip('.')[0]
        df = pd.DataFrame()  
        #     # try:
        if 'products' in data:
                
            for index,i in enumerate(data['products']):  
                # print(index)  
                df.loc[index,'pid'] = i['fnlColorVariantData']['colorGroup']
                df.loc[index,'product_image_url'] = i['fnlColorVariantData']['outfitPictureURL']
                df.loc[index,'brand'] = i['fnlColorVariantData']['brandName']
                try:
                    df.loc[index,'rating'] = i['averageRating']
                except:
                    df.loc[index,'rating'] = None
                df.loc[index,'dp'] = i['price']['value']
                df.loc[index,'mrp'] = i['wasPriceData']['value']
                df.loc[index,'product'] = i['name']
                df.loc[index,'Link'] = 'https://www.ajio.com' + i['url']
                # df.loc[index,'offer price'] = i['offerPrice']['value']
                df.loc[index,'gender'] = i['segmentNameText']
                df.loc[index,'L1'] = i['verticalNameText']
                df.loc[index,'L2'] = i['brickNameText']
                df.loc[index,'primary_image'] = i['images'][0]['url']
                try:
                    df.loc[index,'offer price'] = i['offerPrice']['value']
                except:
                    df.loc[index,'offer price'] = None

                try:
                    df.loc[index,'number of ratings'] = i['ratingCount']
                except:
                    df.loc[index,'number of ratings'] = None
                # df.loc[index,'page'] = page_number
                if 'extraImages' in i:
                    for pic in i['extraImages']:
                        df.loc[index,pic['model']] = pic['images'][0]['url']

            # main_data = pd.concat([main_data,df])
            # except:
            #     print(f'no products at page {pid}')
        else:
            print('no data was available!!')  

            
        return df
    

import math
import requests
import os
import json
import time
import pandas as pd
# import utility as u

def scraping_data(url_firstpart, url_lastpart, path, items,brand):
    '''
        this function scrapes ajio data from its api
        and saves it to path (input in function)
        ouput: saving json file
        return: None
    '''
    start_time = time.time()

    count = 0
    pages = math.ceil(items/45) # because in 1 json file 45 products are present
    main_data = pd.DataFrame()
    main_list = []

    # FIRST ITERATION IN WHICH I GET NUMBER OF PAGES AS WELL
    url = url_firstpart + str(1) + url_lastpart
    response = requests.get(url)
    API_Data = response.json()
    # save data 
    save_object = {f'{brand} - Page no - 1':API_Data}
    main_list.append(save_object)

    # INSTEAD OF SAVING RESPONSE CREATE A CSV DATAFRAME AND SAVE THAT INSTEAD
    df = pd.DataFrame()
    df = json_to_df(API_Data)

    # for counting the number of pages
    count+=1

    main_data = pd.concat([main_data,df])
    pages = int(API_Data['pagination']['totalPages'])

    for j in range(2,pages+1):
        url = url_firstpart + str(j+1) + url_lastpart
        response = requests.get(url)
        API_Data = response.json()

        save_object = {f'{brand} - Page no - {j}':API_Data}
        main_list.append(save_object)

        # INSTEAD OF SAVING RESPONSE CREATE A CSV DATAFRAME AND SAVE THAT INSTEAD
        df = pd.DataFrame()
        df = json_to_df(API_Data)

        if count%5==0:
            time.sleep(1)
            print(f'{str(brand)} pages completed {j+1}')
        count+=1

        main_data = pd.concat([main_data,df])
        # print(f'as of now !!!!!!!! styles count {main_data.shape[0]}')
    print('########## SCRAPING IS COMPLETED ######')
    print("--- %s seconds ---" % (time.time() - start_time))

    return (main_data,main_list)

brand_list = {
  'vero moda': ['https://www.ajio.com/api/category/83?currentPage=2&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&classifier=intent&curated=true&curatedid=vero-moda-4646-42631&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&displayRatings=true',
  4324],
#  'forever new': ['https://www.ajio.com/api/category/forever-new?fields=SITE&currentPage=2&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&classifier=intent&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=true&displayRatings=true',
#   1122],
#  'us polo ass': ['https://www.ajio.com/api/category/83?currentPage=1&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&classifier=intent&curated=true&curatedid=u-s-polo-assn-4357-63541&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=true&is_ads_enable_plp=true&displayRatings=true',
#   13015],
#  'fable street': ['https://www.ajio.com/api/category/83?currentPage=0&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&classifier=intent&curated=true&curatedid=fablestreet-5393-61451&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=true&displayRatings=true',
#   1819],
#  'black scissor': ['https://www.ajio.com/api/search?fields=SITE&currentPage=0&pageSize=45&format=json&query=BLACK%20SCISSOR%3Arelevance&sortBy=relevance&text=BLACK%20SCISSOR&classifier=intent&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&is_ads_enable_plp=true&is_ads_enable_slp=true&showAdsOnNextPage=false&displayRatings=true&segmentIds=',
#   560],
#  'cover story': ['https://www.ajio.com/api/category/83?currentPage=1&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&curated=true&curatedid=coverstory-5327-51251&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=true&displayRatings=true',
#   999],
#  'biba': ['https://www.ajio.com/api/category/83?currentPage=0&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&classifier=intent&curated=true&curatedid=biba-4377-60901&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=true&displayRatings=true',
#   2193],
#  'fashor': ['https://www.ajio.com/api/category/fashor?fields=SITE&currentPage=0&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&classifier=intent&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=true&is_ads_enable_plp=true&displayRatings=true',
#   2989],
#  'stylum': ['https://www.ajio.com/api/category/stylum?fields=SITE&currentPage=0&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&classifier=intent&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=true&displayRatings=true',
#   1002],
#  'only ': ['https://www.ajio.com/api/category/83?currentPage=0&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&classifier=intent&curated=true&curatedid=only-4646-42701&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=true&is_ads_enable_plp=true&displayRatings=true',
#   3350],
#  'kassauly': ['https://www.ajio.com/api/category/83?currentPage=0&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&classifier=intent&curated=true&curatedid=kassually-5394-66591&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=true&displayRatings=true',
#   3075],
#  'allen solly': ['https://www.ajio.com/api/category/allen-solly?fields=SITE&currentPage=0&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&classifier=intent&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=true&is_ads_enable_plp=true&displayRatings=true',
#   4570],
#  'mabish by sonla jain': ['https://www.ajio.com/api/category/mabish-by-sonal-jain?fields=SITE&currentPage=0&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&classifier=intent&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=true&displayRatings=true',
#   727],
#  'styli ': ['https://www.ajio.com/api/search?fields=SITE&currentPage=0&pageSize=45&format=json&query=Styli%3Arelevance&sortBy=relevance&text=Styli&classifier=intent&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&is_ads_enable_plp=true&is_ads_enable_slp=true&showAdsOnNextPage=true&displayRatings=true&segmentIds=',
#   2160],
#  'levis ': ['https://www.ajio.com/api/category/83?currentPage=0&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&classifier=intent&curated=true&curatedid=levis-4141-67361&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=true&is_ads_enable_plp=true&displayRatings=true',
#   2745],
#  'w': ['https://www.ajio.com/api/category/w?fields=SITE&currentPage=0&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&classifier=intent&gridColumns=5&facets=&segmentIds=&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=true&displayRatings=true',
#   3361]
}


  # ajio = stem.ajio('temp')
final_data = pd.DataFrame()
main_list_ = []
for k,v in brand_list.items():
  brnd = k
  url = v[0]
  items = v[1]
  print(brnd)

  ind = url.index('currentPage=')
  url_prt1 = url[:ind+12]
  url_prt2 = url[ind+13:]

  df = pd.DataFrame()
  df,tmp_list = scraping_data(url_prt1, url_prt2,'.',items,brnd)
  main_list_.append(tmp_list)

  final_data = pd.concat([final_data,df])

today = datetime.now().date()
final_data.to_csv(f'ajio_data {today}.csv')


