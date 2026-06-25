-- ============================================================
-- 電商營收趨勢分析 — SQL 版本
-- 與 Python(pandas)清洗流程完全一致,含去重
-- 資料表名假設為 online_retail
-- 語法以 MySQL 為主,其他資料庫的日期函式差異見檔案最後的註解
-- ============================================================


-- ------------------------------------------------------------
-- 共用:清洗後的基礎資料(CTE)
-- 對應 Python:
--   df.drop_duplicates()            -> SELECT DISTINCT *
--   dropna(subset=['CustomerID'])   -> CustomerID IS NOT NULL
--   ~InvoiceNo.startswith('C')      -> InvoiceNo NOT LIKE 'C%'
--   Quantity > 0 / UnitPrice > 0    -> 同條件
-- 清洗後應為 392,692 筆(與 Python 一致)
-- ------------------------------------------------------------
WITH deduped AS (
    SELECT DISTINCT *
    FROM online_retail
),
cleaned AS (
    SELECT *
    FROM deduped
    WHERE CustomerID IS NOT NULL
      AND InvoiceNo NOT LIKE 'C%'
      AND Quantity > 0
      AND UnitPrice > 0
)
-- 驗算用:確認清洗後筆數 = 392,692
SELECT COUNT(*) AS row_count
FROM cleaned;


-- ------------------------------------------------------------
-- 分析 1|月營收趨勢
-- 對應 Python 的 groupby('YearMonth')['TotalPrice'].sum()
-- ------------------------------------------------------------
WITH deduped AS (
    SELECT DISTINCT * FROM online_retail
),
cleaned AS (
    SELECT *
    FROM deduped
    WHERE CustomerID IS NOT NULL
      AND InvoiceNo NOT LIKE 'C%'
      AND Quantity > 0
      AND UnitPrice > 0
)
SELECT
    DATE_FORMAT(InvoiceDate, '%Y-%m')        AS year_month,
    ROUND(SUM(Quantity * UnitPrice), 2)      AS monthly_revenue,
    COUNT(DISTINCT InvoiceNo)                AS orders
FROM cleaned
GROUP BY year_month
ORDER BY year_month;
-- 提醒:最後一個月 2011-12 資料僅到 12/9,屬不完整月份,解讀時要註明。


-- ------------------------------------------------------------
-- 分析 2a|明星商品 Top 10(依營收)
-- 對應 Python 的 product.sort_values('Revenue').head(10)
-- ------------------------------------------------------------
WITH deduped AS (
    SELECT DISTINCT * FROM online_retail
),
cleaned AS (
    SELECT *
    FROM deduped
    WHERE CustomerID IS NOT NULL
      AND InvoiceNo NOT LIKE 'C%'
      AND Quantity > 0
      AND UnitPrice > 0
)
SELECT
    Description,
    ROUND(SUM(Quantity * UnitPrice), 2)      AS revenue,
    SUM(Quantity)                            AS total_quantity,
    COUNT(DISTINCT InvoiceNo)                AS orders
FROM cleaned
GROUP BY Description
ORDER BY revenue DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 分析 2b|銷量 Top 10(依數量)— 用來做「賣最多 ≠ 最賺錢」對比
-- ------------------------------------------------------------
WITH deduped AS (
    SELECT DISTINCT * FROM online_retail
),
cleaned AS (
    SELECT *
    FROM deduped
    WHERE CustomerID IS NOT NULL
      AND InvoiceNo NOT LIKE 'C%'
      AND Quantity > 0
      AND UnitPrice > 0
)
SELECT
    Description,
    SUM(Quantity)                            AS total_quantity,
    ROUND(SUM(Quantity * UnitPrice), 2)      AS revenue
FROM cleaned
GROUP BY Description
ORDER BY total_quantity DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 分析 3a|各國營收貢獻(含 AOV 平均訂單金額)
-- AOV = 總營收 / 訂單數(每「張訂單」的平均金額,標準定義)
-- ------------------------------------------------------------
WITH deduped AS (
    SELECT DISTINCT * FROM online_retail
),
cleaned AS (
    SELECT *
    FROM deduped
    WHERE CustomerID IS NOT NULL
      AND InvoiceNo NOT LIKE 'C%'
      AND Quantity > 0
      AND UnitPrice > 0
)
SELECT
    Country,
    ROUND(SUM(Quantity * UnitPrice), 2)                                AS revenue,
    COUNT(DISTINCT CustomerID)                                         AS customers,
    COUNT(DISTINCT InvoiceNo)                                          AS orders,
    ROUND(SUM(Quantity * UnitPrice) / COUNT(DISTINCT InvoiceNo), 2)    AS aov
FROM cleaned
GROUP BY Country
ORDER BY revenue DESC;


-- ------------------------------------------------------------
-- 分析 3b|各國營收(排除英國)— 看清楚英國以外的市場
-- ------------------------------------------------------------
WITH deduped AS (
    SELECT DISTINCT * FROM online_retail
),
cleaned AS (
    SELECT *
    FROM deduped
    WHERE CustomerID IS NOT NULL
      AND InvoiceNo NOT LIKE 'C%'
      AND Quantity > 0
      AND UnitPrice > 0
)
SELECT
    Country,
    ROUND(SUM(Quantity * UnitPrice), 2)                                AS revenue,
    COUNT(DISTINCT InvoiceNo)                                          AS orders,
    ROUND(SUM(Quantity * UnitPrice) / COUNT(DISTINCT InvoiceNo), 2)    AS aov
FROM cleaned
WHERE Country <> 'United Kingdom'
GROUP BY Country
ORDER BY revenue DESC;


-- ============================================================
-- 不同資料庫的日期函式差異(把 DATE_FORMAT 那行換掉即可)
--   MySQL:       DATE_FORMAT(InvoiceDate, '%Y-%m')
--   SQLite:      strftime('%Y-%m', InvoiceDate)
--   PostgreSQL:  TO_CHAR(InvoiceDate, 'YYYY-MM')
--   BigQuery:    FORMAT_DATE('%Y-%m', InvoiceDate)
-- ============================================================
