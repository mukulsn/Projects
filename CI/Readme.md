**CI PROJECT**

CI - Competitive Intelligence Project

AIM : This project is used by Big commerce and E commerce companies to understand marketplace curation and their pricing strategies.

What Can be Achieved?
Through Competitive Intelligence we can understand multiple aspects of competitors.
1. Catalogue width and depth
2. Brand Coverage
3. New Selection Rate
4. Customer Views of products
5. Pricing strategy

There are multiple aspect in which we can deep dive further and understand how these data points can help a Ecommerce company create strategy.

------

This Project is comparing Prices from 2 Ecommerce Platform,
Project is divided into multiple tasks.

1. Data Gathering
2. Storage of data
3. Downloading resources for Product Matching
4. Creating Embedding and storing them
5. Matching the Nearest Product

**Data Gathering:** 
- Web Scraper is required to scrape gather data points from Ecommerce Websites
- We are targeting only 1 brand in this project, but the framework is designed in a way that we can easily scale it to more brands

**Storage:**
- Scraped data needs to be stored and accessible in common location
- Embedding also need to be stored for further working on them
- We are using Nearest Neigbours technique to match the products. so Distance and indices files also needs to be stored

**Download:**
- Bulk image downloading is required

**Embedding Creation:**
- Embeddings are generated using SigLip, so GPU is required to create them to fast process the generation.
- it is approximately ~15-20 faster to produce Embeddings through GPU than CPU, depending on which GPU you are using. P100 is used to generate embeddings.

**Matching Products:**
- We are using FAISS Facebook AI Similarity Search, it is compatible to work with CPU and GPU both.
- FAISS can be quickly used to compare embeddings and calculate similarity in between them

![image](https://github.com/user-attachments/assets/9c2ddf40-f715-4f60-a3b2-b3bf12b424dd)






Files in S3 bucket : https://us-east-1.console.aws.amazon.com/s3/buckets/ci-ml?region=us-east-1&bucketType=general&prefix=Production+files/
