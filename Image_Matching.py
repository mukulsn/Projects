# # AIM : IMAGES DOWNLOAD

# 1.Extract data 
# 2.convert to proper dataframe format
# 3.download images (think it is the most error prone code block) - solve this with try and except later
# 4.save images to directory

import boto3
import pandas as pd
import numpy as np
import csv
import requests
import time
import asyncio 
import aiohttp
import aiofiles
import os

# import boto3

# def s3_operations(bucket_name, source_key):
#     s3 = boto3.client('s3',
#                       aws_access_key_id=aws_access_key_id,
#                       aws_secret_access_key=aws_secret_access_key)
                      
#     s3.download_file(bucket_name,source_key,'ajio_data 2024-12-07.csv')

ajio = pd.read_csv('/kaggle/working/ajio_data 2024-12-07.csv')

# converting dataframe
ajio_image_list = []
cols = ['model1', 'model2', 'model3','model4', 'model5', 'model6', 'model7', 'model8', 'model9', 'model10']
for ind,i in ajio.head(10).iterrows():
    for ind_,k in enumerate(cols):
        if not pd.isna(i[k]):
            # ajio_image_dict[i['pid']+'___'+f'image_{ind_+1}'] = i[k]
            key_ = f'{i["pid"]}___image_{ind_+1}'
            ajio_image_list.append((key_,i[k]))
    
len(ajio_image_list)

# dataframe to accomodate new structure
ajio_df = pd.DataFrame()
ajio_df['pid_modified'] = [x[0] for x in ajio_image_list]
ajio_df['pics'] = [x[1] for x in ajio_image_list]
ajio_df['pid'] = [x.split('___')[0] for x in ajio_df['pid_modified']]
ajio_df.drop_duplicates(subset='pid_modified').to_csv('temp_data.csv')
ajio_df = ajio_df.drop_duplicates(subset='pid_modified')

# Code to help if download image code error occurs
downloaded_pics = [x.replace('.jpg','') for x in os.listdir('/kaggle/working/ajio_pics')]
ajio_df = ajio_df[~ajio_df.pid_modified.isin(downloaded_pics)]
ajio_df.shape

bucket_name = 'ci-ml'
source_key = 'staging_scripts_for_project/donwload_image.py'

# source file to download images
s3 = boto3.client('s3',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)
                  
s3.download_file(bucket_name,source_key,'donwload_image.py')

# running image downloading script
# %%time
# !python donwload_image.py

### download_image.py script


df= pd.read_csv('/kaggle/working/temp_data.csv')

#supporting functions
async def download_image(session,file_name, url, save_path):
    async with session.get(url) as response:
        if response.status == 200:
            image_data = await response.read()
            # file_name = url.split('/')[-1]
            file_name = str(file_name) + '.jpg'
            file_path = os.path.join(save_path, file_name)
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(image_data)
            # print(f"Downloaded {file_name}")
        else:
            print(f"Failed to download image from {url}")

#supporting functions
async def main(image_urls, save_path):
    timeout = aiohttp.ClientTimeout(total=1800)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [download_image(session, url[0],url[1], save_path) for url in image_urls]
        await asyncio.gather(*tasks)


def downloading_images(df):
    '''
        trying downloading images asynchronously and compare with multiprocessing image 
        downloading.

    '''

    start_time = time.time()

    image_urls = [x for x in zip(df['pid_modified'],df['pics'])]    
    # save_path = "./downloaded_images"
    os.makedirs('ajio_pics', exist_ok=True)
    asyncio.run(main(image_urls, 'ajio_pics'))

    print('##### IMAGE DOWNLOADING COMPLETED ####')
    print("--- %s seconds ---" % (time.time() - start_time))

downloading_images(df)

# Embedding Generation

# testing Image
from PIL import Image

url = ajio_image_list[1][1]
# image = Image.open(requests.get(url, stream=True).raw)
image = Image.open('/kaggle/working/ajio_pics/463760857_orange___image_1.jpg')

# images are way too large that make this notebook too large as well
# downscale
width = 300
ratio = (width / float(image.size[0]))
height = int((float(image.size[1]) * float(ratio)))
img = image.resize((width, height), Image.Resampling.LANCZOS)
display(img)

# supporting Functions
def add_vector(embedding, index):
    vector = embedding.detach().cpu().numpy()
    vector = np.float32(vector)
    faiss.normalize_L2(vector)
    index.add(vector)

def embed_siglip(image):
    with torch.no_grad():
        inputs = processor(images=image, return_tensors="pt").to(device)
        image_features = model.get_image_features(**inputs)
        return image_features

# Creating vectors and adding to Faiss Index

from PIL import Image
from torchvision import transforms
from tqdm.autonotebook import tqdm

# initialize the index with the size matching of embeddings out from the model
index = faiss.IndexFlatL2(768)

#storage of embeddings
emebd_store = {}
# read the image and add vector
for elem in tqdm(ajio_df['pid_modified']):
  # url = elem[1]
  image = Image.open(f'/kaggle/working/ajio_pics/{elem}.jpg')
  clip_features = embed_siglip(image) # add here pid too
  emebd_store[elem] = clip_features
  add_vector(clip_features,index) # save data as much you can
  # break

# Image similarity Inference
# test image 
# image of a man
url = ajio_image_list[10][1]
image = Image.open(requests.get(url, stream=True).raw)
display(image)

# query image 
with torch.no_grad():
  inputs = processor(images=image, return_tensors="pt").to(device)
  input_features = model.get_image_features(**inputs)

input_features = input_features.detach().cpu().numpy()
input_features = np.float32(input_features)
faiss.normalize_L2(input_features)
distances, indices = index.search(input_features, 3)

# show results
for elem in indices[0]:
  url = ajio_image_list[elem][1]
  image = Image.open(requests.get(url, stream=True).raw)
  width = 300
  ratio = (width / float(image.size[0]))
  height = int((float(image.size[1]) * float(ratio)))
  img = image.resize((width, height), Image.Resampling.LANCZOS)
  display(img)
