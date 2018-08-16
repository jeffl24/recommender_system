import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
# Display as many columns as possible
pd.options.display.max_columns = 999
shopify_data = pd.read_csv("shopify_orders_export_20180207.csv",
                           low_memory=False,
                           dtype={'Lineitem sku': 'str', 'Name': 'str'},
                           parse_dates = ['Paid at', 'Created at'])

import requests
import json
full_size_skus = products_sales_count[~products_sales_count['child_sku'].str.endswith(('9', '7', '6', '8'))]['child_sku'].unique()
sku_list = shopify_data_debundled['child_sku'].unique()
all_sku_reviews = pd.DataFrame()
for sku in full_size_skus:
    single_query = requests.get('https://pcsg-reviews-api.paulaschoice.tech/product/{}'.format(sku)).text
    single_json = pd.io.json.json_normalize(json.loads(single_query))
    all_sku_reviews = all_sku_reviews.append(single_json)

# all_sku_reviews.to_csv('all_sku_reviews.csv')
reviews_sku_rating = all_sku_reviews[['sku', 'rating']]
reviews_by_sku = pd.DataFrame(reviews_sku_rating.groupby('sku')['rating'].mean())
reviews_by_sku['review_count'] = pd.DataFrame(reviews_sku_rating.groupby('sku')['rating'].count())
reviews_by_sku.sort_values('review_count', ascending=False)

# plt.figure(figsize=(10,4))
# reviews_by_sku['review_count'].hist(bins=30)
# plt.title('Histogram of count of reviews for products');
#
# plt.figure(figsize=(10,4))
# reviews_by_sku['rating'].hist(bins=30)
# plt.title('Histogram of review scores');
#
# import seaborn as sns
# sns.jointplot(x='rating',y='review_count',data=reviews_by_sku,alpha=0.5)
# plt.title('Average rating vs. number of reviews for each product', x=-3, y=1.2);
#
user_rating_matrix = pd.read_csv('all_sku_reviews.csv')
user_rating_matrix = user_rating_matrix [['reviewer_email', 'sku', 'rating']].drop_duplicates(subset= ['reviewer_email', 'sku'])
user_rating_pivot = user_rating_matrix.pivot(index='reviewer_email', columns='sku', values='rating')

user_rating_6002 = user_rating_pivot[6002]
user_rating_6002

similar_to_6002 = pd.DataFrame(user_rating_pivot.corrwith(user_rating_6002),columns=['Correlation'])
similar_to_6002.dropna().sort_values('Correlation', ascending=False)
