import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os

zip_file_path = 'dataset.zip'

if os.path.exists(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall('dataset')  
    df = pd.read_csv('dataset/olist_customers_dataset.csv')
    df1 = pd.read_csv('dataset/olist_orders_dataset.csv')
else:
    st.error(f'File {zip_file_path} not found')

# Data preprocessing
df = df.drop(['customer_unique_id', 'customer_zip_code_prefix', 'customer_city'], axis=1)
df1 = df1.drop(['order_status', 'order_approved_at', 'order_delivered_carrier_date', 'order_estimated_delivery_date', 'order_delivered_customer_date'], axis=1)

# Streamlit interface
st.title('E-commerce Data Analysis')

# 1. Registered customers in each state
state_counts = df['customer_state'].value_counts()

st.subheader('Registered Customers per State')
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(state_counts.index, state_counts.values, color='skyblue')
ax.set_title('Registered Customers')
ax.set_xlabel('State')
ax.set_ylabel('Customer Counts')
ax.set_xticks(state_counts.index)
ax.set_xticklabels(state_counts.index, rotation=45)
st.pyplot(fig)

st.write("From the customer dataset, it can be analyzed that the largest number of registered customers are in the SP state.")

# 2. Number of purchases each year
df1['order_purchase_timestamp'] = pd.to_datetime(df1['order_purchase_timestamp'])
df1['Year'] = df1['order_purchase_timestamp'].dt.year
yearly_orders = df1['Year'].value_counts().sort_index()

st.subheader('Number of Purchases Each Year')
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(yearly_orders.index, yearly_orders.values, color='lightgreen')
ax.set_title('Number of Purchases Each Year')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Purchases')
ax.set_xticks(yearly_orders.index)
st.pyplot(fig)

st.write("From the orders dataset, it can be analyzed that the number of purchases tends to increase every year and the highest number of purchases received was in 2018.")

# 3. Number of purchases per month for each year
df_2016 = df1[df1['order_purchase_timestamp'].dt.year == 2016]
df_2017 = df1[df1['order_purchase_timestamp'].dt.year == 2017]
df_2018 = df1[df1['order_purchase_timestamp'].dt.year == 2018]

df_2016['Month'] = df_2016['order_purchase_timestamp'].dt.month
df_2017['Month'] = df_2017['order_purchase_timestamp'].dt.month
df_2018['Month'] = df_2018['order_purchase_timestamp'].dt.month

monthly_purchases_2016 = df_2016['Month'].value_counts().reindex(range(1, 13), fill_value=0).sort_index()
monthly_purchases_2017 = df_2017['Month'].value_counts().reindex(range(1, 13), fill_value=0).sort_index()
monthly_purchases_2018 = df_2018['Month'].value_counts().reindex(range(1, 13), fill_value=0).sort_index()

st.subheader('Number of Purchases in 2016-2018')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_purchases_2016.index, monthly_purchases_2016.values, marker='o', color='green', linestyle='-', label='2016')
ax.plot(monthly_purchases_2017.index, monthly_purchases_2017.values, marker='o', color='blue', linestyle='-', label='2017')
ax.plot(monthly_purchases_2018.index, monthly_purchases_2018.values, marker='o', color='red', linestyle='-', label='2018')
ax.set_title('Number of Purchases in 2016-2018')
ax.set_xlabel('Month')
ax.set_ylabel('Number of Purchases')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax.set_ylim(0, 8000)
ax.legend(title="Year")
st.pyplot(fig)

st.write("The first graph is for question 1, shows the number of purchases from 2016 to 2018, with fluctuations clearly visible in each year. In 2016 shows a stable number of purchases although there are some months with no data, while 2017 saw a significant increase, especially in certain months, before experiencing a significant decline in December. While in 2018 the graph tends to show a decline.")

# 4. Number of unique customers placing orders per state each year
merged_data = pd.merge(df1, df, on='customer_id')
merged_data['Year'] = merged_data['order_purchase_timestamp'].dt.year
merged_data['Month'] = merged_data['order_purchase_timestamp'].dt.month

state_customers = merged_data.groupby(['Year', 'customer_state'])['customer_id'].nunique().unstack(fill_value=0)

st.subheader('Number of Customers per State in 2016-2018')
fig, ax = plt.subplots(figsize=(15, 8))
x = np.arange(len(state_customers.columns))  
bar_width = 0.25

ax.bar(x - bar_width, state_customers.loc[2016], width=bar_width, label='2016', color='green')
ax.bar(x, state_customers.loc[2017], width=bar_width, label='2017', color='blue')
ax.bar(x + bar_width, state_customers.loc[2018], width=bar_width, label='2018', color='red')

ax.set_title('Number of Customers per State in 2016-2018')
ax.set_xlabel('State')
ax.set_ylabel('Number of Unique Customers')
ax.set_xticks(x)
ax.set_xticklabels(state_customers.columns, rotation=45)
ax.set_ylim(0, 25000)
ax.legend(title="Year")
st.pyplot(fig)

st.write("The second graph is for question 2, shows a significant variation in the distribution of unique customers across states. Some state, such as MG, RJ, SP showing significantly higher customer numbers in 2017 and 2018.")

st.header("CONCLUSION")
st.subheader("QUESTION 1 : Which month had the highest number of purchases in 2017?")
st.write("Based on the visualized graph 1 it can be seen that purchases in 2017 were the best, besides the fact that 2017 most likely had the most complete data for each month, but in 2017 the graph also tended to increase compared to the previous or subsequent years. It can be seen that the highest increase was in November with a total of 7544 purchases. So it can be concluded that the month with the highest number of purchases in 2017 was November.")
st.subheader("QUESTION 2 : Which state have the largest source of customers in 2017?")
st.write("Based on the visualized graph 2, it can be seen that the largest number of customers is in the SP state. However, not only in 2017, but in 2016 and 2018 SP also ranked at the top for the largest number of customers. In 2017, the SP state reached 17760 customers, this is an increase in the number of customers in SP state, because previously in 2016 the number of customers in SP was only 115, and then there was a significant increase in 2018 so that it reached 23871 customers.")
