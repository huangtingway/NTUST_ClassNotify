# NTUST_ClassNotify
About: 使用網頁爬蟲擷取課程查詢系統選課人數，出現未額滿課程時自動通知

## 安裝步驟 
安裝chrome driver：https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.61/win32/chromedriver-win32.zip (windows)  

開啟python IDE，在終端機輸入以下命令：
- 網頁爬蟲：pip install selenium==3.3.1
- GUI：pip install tk
- 自動通知：pip install win10toast

## 使用方式
1. 在pyton IDE執行gui.py
2. 在input chrome driver path輸入chromedriver-win32.exe檔案路徑
3. 在input course code輸入想搜尋的課程代碼，點擊add
4. 點擊start search開始自動搜尋
5. 當未額滿課程改變時，程式自動發出通知，所有可選課程自動複製到剪貼簿，輸入windows + v開啟
6. 所有未額滿課程同時更新在available course
7. 在search class點擊任意課程代碼，再點擊delete即可刪除搜尋課程
   
## demo
