import pandas as pd
import requests
import json

#Import file to obtain list of full size sku
shopify_data = pd.read_csv("pcsg_reviews\shopify_orders_export_20180207.csv",
                           low_memory=False,
                           dtype={'Lineitem sku': 'str', 'Name': 'str'},
                           parse_dates = ['Paid at', 'Created at'])
full_size_skus = shopify_data[~shopify_data['Lineitem sku'].str.endswith(('9', '7', '6', '8'), na=False)]['Lineitem sku'].unique()

all_sku_reviews = pd.DataFrame()
for sku in full_size_skus:
    single_query = requests.get('https://pcsg-reviews-api.paulaschoice.tech/product/{}'.format(sku)).text
    single_json = pd.io.json.json_normalize(json.loads(single_query))
    all_sku_reviews = all_sku_reviews.append(single_json)

# all_sku_reviews.to_csv('file_name.csv')
# Draw correlation
