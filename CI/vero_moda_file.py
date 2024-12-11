
import requests 
import urllib.request
import numpy as np
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import os
import json
import math
from datetime import datetime
import boto3

start_time = time.time()

def split_url(string):
    # Split the string by commas
    split_string = string.split(',')

    # Remove the single quotes from each element
    cleaned_strings = [s.strip("'") for s in split_string]
    return cleaned_strings

def to_s3(bucket,file,date):
    # s3 = boto3.resource('s3')
    # BUCKET = "ci-ml"
    # file = 'ajio_data 2024-12-07.csv'
    # s3_folder = '2024-12-07/'

    # s3.Bucket(BUCKET).upload_file(file, s3_folder+file)
    # print(f'uploaded to s3 {s3_folder+file}')

    s3 = boto3.resource('s3')
    BUCKET = bucket
    file = file
    s3_folder = f'data/date={date}/'

    s3.Bucket(BUCKET).upload_file(file, s3_folder+file)
    print(f'uploaded to s3 {s3_folder+file}')


def convert_to_df(soup):
    # This have info about style
    _ = soup.find_all('div',class_='product-layout product-item product-grid col-xs-6 col-md-4 col-lg-4')

    df= pd.DataFrame()
    for ind,product in enumerate(_):
        name = product.find_all('a', class_='single-product')[1].text.strip()
        try:
            price = product.find('span', class_='price-new').text.strip()
            df.loc[ind,'price'] = price
        except:
            price = product.find('p', class_='price').text.strip()
            df.loc[ind,'price'] = price
        try:
            price_old = product.find('span', class_='price-old').text.strip()
            df.loc[ind,'price_old'] = price_old
        except:
            pass
        pdp_url = product.find('div',class_='img_slider veromoda-owl')['data-href']
        try:
            special_tag = product.find('span',id='organic').text
            df.loc[ind,'special_tag'] = special_tag
        except:
            pass
        try:
            special_tag_2 = product.find('div',class_='promotion-text online-exclusive').text.strip()
            df.loc[ind,'special_tag_2'] = special_tag_2
        except:
            pass

        # All images
        all_images = product.find('div',class_='img_slider veromoda-owl')['data-imageurl']
        all_img_list = split_url(all_images)
        try:
            sale_discount = product.find('span', class_='sale sale-percentage').text.strip()
            df.loc[ind,'sale_discount'] = sale_discount
        except:
            pass

        df.loc[ind,'name'] = name
        for ind_new,i in enumerate(all_img_list):
            df.loc[ind,f'image_{ind_new+1}'] = i 

    return df

if __name__ == '__main__':
    print('script started')

    res = requests.get('https://www.veromoda.in/vm-all-product&sort=sort_order&order=desc&page=1')
    soup = BeautifulSoup(res.text, features="html.parser")

    # all styles
    all_styles = int(soup.find('span', class_='category-total-item').text.strip())
    pages = math.ceil(all_styles/24)
    print(f'total pages {pages}')

    main_df = pd.DataFrame()

    _ = convert_to_df(soup)
    main_df = pd.concat([main_df,_])

    # now for other pages
    for ind,i in enumerate(range(2,pages)):
        
        res = requests.get('https://www.veromoda.in/vm-all-product&sort=sort_order&order=desc&page=1')
        soup = BeautifulSoup(res.text, features="html.parser")

        _ = convert_to_df(soup)
        main_df = pd.concat([main_df,_])  

        if ind%5 == 0:
            print(f'for loop {ind}')
            time.sleep(5)

    today = datetime.now().date()
    file_name = f'vero_moda_website_{today}.csv'
    main_df.to_csv(file_name)

    to_s3('ci-ml',file_name,today)

    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_minutes = elapsed_time / 60

    print(f"Script execution time: {elapsed_minutes:.2f} minutes")

