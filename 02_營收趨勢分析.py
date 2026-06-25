"""
專案二:電商營收趨勢分析
======================================
功能:清洗資料 → 月營收走勢 → 明星商品 → 各國貢獻 → 輸出給 Tableau
資料來源:Kaggle UCI Online Retail Dataset
作者:[金予晨]
"""

import pandas as pd

# ============================================================
# Step 1. 讀取與清洗(與專案一一致,含去重)
# ============================================================
df = pd.read_excel('Online Retail.xlsx')   # 換成你的檔名路徑

df = df.drop_duplicates()
df = df.dropna(subset=['CustomerID'])
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]

df['CustomerID'] = df['CustomerID'].astype(int)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)

# 匯出清洗後明細,供 Tableau 直接使用
df.to_csv('cleaned_retail.csv', index=False, encoding='utf-8-sig')

# ============================================================
# Step 2. 月營收走勢(含月增率)
#   註:最後一個月 2011-12 資料僅到 12/9,屬不完整月份
# ============================================================
monthly = df.groupby('YearMonth')['TotalPrice'].sum().reset_index()
monthly['MoM_growth_%'] = (monthly['TotalPrice'].pct_change() * 100).round(1)
print('=== 月營收走勢 ===')
print(monthly.to_string(index=False))

# ============================================================
# Step 3. 明星商品(營收 Top 10 vs 銷量 Top 10)
# ============================================================
product = df.groupby('Description').agg(
    Revenue=('TotalPrice', 'sum'),
    Quantity=('Quantity', 'sum'),
    Orders=('InvoiceNo', 'nunique')
).reset_index()

print('\n=== 營收 Top 10 商品 ===')
print(product.sort_values('Revenue', ascending=False).head(10).to_string(index=False))

print('\n=== 銷量 Top 10 商品 ===')
print(product.sort_values('Quantity', ascending=False).head(10).to_string(index=False))

# ============================================================
# Step 4. 各國貢獻(含平均訂單金額 AOV)
#   AOV = 總營收 / 訂單數
# ============================================================
country = df.groupby('Country').agg(
    Revenue=('TotalPrice', 'sum'),
    Customers=('CustomerID', 'nunique'),
    Orders=('InvoiceNo', 'nunique')
).reset_index()
country['AOV'] = (country['Revenue'] / country['Orders']).round(2)
country = country.sort_values('Revenue', ascending=False)

print('\n=== 各國營收(前 10)===')
print(country.head(10).to_string(index=False))

print('\n=== 各國營收(排除英國,前 10)===')
print(country[country['Country'] != 'United Kingdom'].head(10).to_string(index=False))
