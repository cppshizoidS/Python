import pandas as pd
df = pd.read_csv('file.csv')
df

df.head()

df.tail(10)

df.Product

df['Product']

df[['Product', 'Quantity Ordered', 'Price Each']]

df['Total'] = df['Price Each'] * df['Quantity Ordered']

df

df.rename(columns={
    'Order ID': 'Order_id',
    'Quantity Ordered': 'Quantity',
    'Price Each': 'Price',
    'Order Date': 'Order_date',
    'Purchase Address': 'Address'
}, inplace=True)

df

df_curr = pd.read_html('https://buhgalter911.com/spravochniki/kursy-stavki-indeksy/kursivalut-nbu.html')
df_curr

df_curr[0]
