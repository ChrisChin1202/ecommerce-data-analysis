# ecommerce-data-analysis
電商 RFM 客戶分群與營收趨勢分析
電商數據分析:顧客分群與營收趨勢

使用 Kaggle 公開電商交易資料(UCI Online Retail),完成兩個從資料清洗、分析到商業建議的完整專案。涵蓋 Python、SQL、Tableau、Power BI 四項技能。


作者:[金予晨] ｜ 淡江大學 管理科學系 ｜  目標職位:數據分析師



📊 專案總覽

專案分析角度工具成果顧客 RFM 分群客戶Python + Power BI客戶分 8 群,提出差異化行銷建議營收趨勢分析營收Python + SQL + Tableau月趨勢、明星商品、市場貢獻分析

🔗 Tableau 互動儀表板:https://public.tableau.com/app/profile/chinyuchen/viz/_17822938018340/1


🗂️ 檔案說明

檔案內容01_RFM分群分析.py資料清洗、RFM 計算、評分與客群分群02_營收趨勢分析.py月營收、明星商品、各國貢獻分析營收趨勢分析_SQL查詢.sql與 Python 一致的 SQL 查詢(含去重)


🧹 資料處理

原始資料約 54.2 萬筆,經以下清洗後保留 39.3 萬筆:


移除完全重複的列
移除無客戶歸戶(CustomerID 缺失)
移除退貨單(InvoiceNo 以 C 開頭)
移除數量 / 單價 ≤ 0 的異常值



資料品質註記:最後一個月(2011/12)資料僅到 12/9,屬不完整月份,分析時已標註避免誤判。




🔍 主要發現

專案一|顧客 RFM 分群


「重要價值客戶」僅佔 26.3% 人數,卻貢獻 66.5% 營收(帕累托效應)。
「無法流失客戶」(過去平均消費 4.9 次、近期已 137 天未回購)是投資報酬最高的挽回對象。
針對 8 個客群提出差異化行銷策略(VIP 維繫、回購培養、流失挽回)。


專案二|營收趨勢分析


營收下半年明顯成長,Q4 為旺季,11 月達高峰。
營收高度集中在英國本土市場;部分海外市場客單價較高,具拓展潛力。
少數高單價商品貢獻多數營收,可作為選品依據。



🛠️ 使用技術


Python(pandas):資料清洗、RFM 計算、彙總分析
SQL:清洗與彙總的等效查詢(支援 MySQL / SQLite / PostgreSQL / BigQuery)
Tableau:營收趨勢互動儀表板(已發佈)
Power BI:RFM 客戶分群儀表板



📥 資料來源

UCI Online Retail Dataset(Kaggle)
https://www.kaggle.com/datasets/jihyeseo/online-retail-data-set-from-uci-ml-repo


因原始資料檔較大,未上傳至本倉庫;請自行下載 Online Retail.xlsx 並與程式放在同一資料夾後執行。


