

import streamlit as st
import pandas as pd
import requests
from PIL import Image

# Try 3
def display_product_info(product_name):
    selected_product = df[df['ajio_pid_modified'] == product_name]
    image_url1 = selected_product['pics_x'].values[0]
    image_url2 = selected_product['pics_y'].values[0]

    # if selected_product['dp'] < selected_product['vero_moda_dp']:
    #     winner = "E-commerce 1"
    # elif selected_product['dp'] < selected_product['vero_moda_dp']:
    #     winner = "E-commerce 2"
    # else:
    #     winner = "Both are equally priced"

    # Fetch images
    response1 = requests.get(image_url1, stream=True)
    response2 = requests.get(image_url2, stream=True)

    if response1.status_code == 200 and response2.status_code == 200:
        img1 = Image.open(response1.raw)
        img2 = Image.open(response2.raw)

        # Resize images to a fixed size
        img1 = img1.resize((300, 350))
        img2 = img2.resize((300, 350))

        # if selected_product['dp'] < selected_product['vero_moda_dp']:
        #     winner = "E-commerce 1"
        # elif selected_product['dp'] < selected_product['vero_moda_dp']:
        #     winner = "E-commerce 2"
        # else:
        #     winner = "Both are equally priced"

        # st.markdown(f"<h2 style='color: green; text-align: center;'>{winner} wins!</h2>", unsafe_allow_html=True)

        # st.image([img1, img2], width=200)
        # Create two columns for images
        col1, col2 = st.columns(2)

        with col1:
            with st.container():
                st.image(img1, caption=f"AJIO Platform:{selected_product['name'].values[0]}")
                st.write(f"**Price:** ₹{selected_product['dp'].values[0]}")

        with col2:
            with st.container():
                st.image(img2, caption=f"**Vero Moda platform:** {selected_product['vero_moda_product_name'].values[0]}")
                st.write(f"**Price:** ₹{selected_product['vero_moda_dp'].values[0]}")

        # with col1:
        #     st.image(img1, caption=f"**E-commerce 1: {selected_product['name'].values[0]}**")
        #     st.write(f"**Price:** {selected_product['dp'].values[0]}")

        # with col2:
        #     st.image(img2, caption=f"E-commerce 2: {selected_product['vero_moda_product_name'].values[0]}")
        #     st.write(f"**Price:** {selected_product['vero_moda_dp'].values[0]}")

    st.write(f"**Product Name:** {selected_product['name'].values[0]}")
    st.write(f"**Price on AJIO Platform:** {selected_product['dp'].values[0]} and MRP {selected_product['mrp'].values[0]}")
    st.write(f"**Price on Vero Moda platform:** {selected_product['vero_moda_dp'].values[0]} and MRP {selected_product['vero_moda_mrp'].values[0]}")

# Assuming your CSV has columns: 'Product Name 1', 'Image URL 1', 'Price 1', 'Image URL 2', 'Price 2'
df = pd.read_csv('final result for production.csv')

# Create a select box to choose a product
product_name = st.selectbox('Select a Product', [(df['ajio_pid_modified'][i], df['name'][i]) for i in range(len(df))])

# Display the product information
display_product_info(product_name[0])

#%% 
# Try 1

# import streamlit as st
# import pandas as pd

# # Read the CSV file
# df = pd.read_csv('product_mapping.csv')

# # Assuming your image filenames are in a column named 'Image Filename'
# # and are stored in the same directory as your script

# def display_product_info(product_name):
#     selected_product = df[df['Product Name 1'] == product_name]
#     image_filename = selected_product['Image Filename'].values[0]
#     image_path = f"images/{image_filename}"  # Adjust the path as needed

#     st.write(f"**Product Name:** {selected_product['Product Name 1'].values[0]}")
#     st.image(image_path)
#     st.write(f"**Price on E-commerce 1:** {selected_product['price 1'].values[0]}")
#     st.write(f"**Price on E-commerce 2:** {selected_product['price 2'].values[0]}")

# # Create a select box to choose a product
# product_name = st.selectbox('Select a Product', df['Product Name 1'].unique())

# # Display the product information
# display_product_info(product_name)

### TRY 2 

# import streamlit as st
# import pandas as pd

# # Read the CSV file
# df = pd.read_csv('product_mapping.csv')

# def display_product_info(product_name):
#     selected_product = df[df['Product Name 1'] == product_name]
#     image_filename = selected_product['Image Filename'].values[0]
#     image_path = f"images/{image_filename}"  # Adjust the path as needed

#     st.image(image_path)
#     st.write(f"**Product Name:** {selected_product['Product Name 1'].values[0]}")
#     st.write(f"**Price on E-commerce 1:** {selected_product['price 1'].values[0]}")
#     st.write(f"**Price on E-commerce 2:** {selected_product['price 2'].values[0]}")

# # Create a select box to choose a product
# product_name = st.selectbox('Select a Product',
#     [(df['Product Name 1'][i], df['Image Filename'][i]) for i in range(len(df))])

# # Display the product information
# display_product_info(product_name[0])

