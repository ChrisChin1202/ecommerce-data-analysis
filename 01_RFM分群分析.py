"""
專案一:電商顧客 RFM 分群分析
======================================
功能:讀取原始交易資料 → 清洗 → 計算 RFM → 評分與分群 → 輸出結果
資料來源:Kaggle UCI Online Retail Dataset
作者:[金予晨]
"""

import pandas as pd

# ============================================================
# Step 1. 讀取資料
# ============================================================
df = pd.read_excel('Online Retail.xlsx')   # 換成你的檔名路徑

# ============================================================
# Step 2. 資料清洗
#   - 移除完全重複的列
#   - 移除無客戶歸戶(CustomerID 缺失)
#   - 移除退貨單(InvoiceNo 以 C 開頭)
#   - 移除數量 / 單價 <= 0 的異常值
# ============================================================
before = len(df)

df = df.drop_duplicates()
df = df.dropna(subset=['CustomerID'])
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]

df['CustomerID'] = df['CustomerID'].astype(int)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

print(f'清理前:{before:,} 筆 → 清理後:{len(df):,} 筆')

# ============================================================
# Step 3. 計算 RFM
#   R(Recency)  最近一次消費距今天數,越小越好
#   F(Frequency)消費次數(不重複訂單數),越多越好
#   M(Monetary) 累積消費金額,越多越好
# ============================================================
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)   # 以最後交易日 +1 天當「今天」

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,   # Recency
    'InvoiceNo': 'nunique',                                     # Frequency
    'TotalPrice': 'sum'                                         # Monetary
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

# ============================================================
# Step 4. RFM 評分(1~5 分)
#   R:越近分數越高(反向)
#   F:用 rank 避免大量重複值導致 qcut 失敗
#   M:越大分數越高
# ============================================================
rfm['R_score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['M_score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)

# ============================================================
# Step 5. 客群分群(依 R 與 F 分數)
# ============================================================
def segment(row):
    r, f = row['R_score'], row['F_score']
    if r >= 4 and f >= 4:
        return '重要價值客戶'
    elif r >= 4 and f >= 2:
        return '潛力客戶'
    elif r >= 4 and f == 1:
        return '新客戶'
    elif r == 3 and f >= 3:
        return '需維繫客戶'
    elif r <= 2 and f >= 4:
        return '無法流失客戶'
    elif r <= 2 and f >= 2:
        return '瀕臨流失客戶'
    elif r <= 2 and f == 1:
        return '流失客戶'
    else:
        return '一般客戶'

rfm['Segment'] = rfm.apply(segment, axis=1)

# ============================================================
# Step 6. 輸出結果(給 Power BI / Tableau 使用)
# ============================================================
rfm.to_csv('RFM_result.csv', index=False, encoding='utf-8-sig')
print(f'已輸出 RFM_result.csv,共 {len(rfm):,} 位客戶')

# 各客群摘要
summary = rfm.groupby('Segment').agg(
    客戶數=('CustomerID', 'count'),
    平均Recency=('Recency', 'mean'),
    平均Frequency=('Frequency', 'mean'),
    總營收=('Monetary', 'sum')
).round(1)
summary['人數佔比%'] = (summary['客戶數'] / len(rfm) * 100).round(1)
summary['營收佔比%'] = (summary['總營收'] / rfm['Monetary'].sum() * 100).round(1)
print(summary.sort_values('總營收', ascending=False))
