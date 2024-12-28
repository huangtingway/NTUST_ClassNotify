# NTUST_ClassNotify
About: 使用網頁爬蟲擷取課程查詢系統選課人數，出現未額滿課程時程式自動發出通知

## 安裝說明 
1. 安裝chrome driver：https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.61/win32/chromedriver-win32.zip (windows)  
2. 開啟python IDE，在終端機輸入以下命令：
- 網頁爬蟲：pip install selenium==3.3.1
- GUI：pip install tk
- 自動通知：pip install win10toast
  
## demo
<video src="https://github.com/huangtingway/NTUST_ClassNotify/assets/92153423/542256bb-9ab5-4a20-98f7-4504abd783df" width="100%" controls></video>

## 使用方式
1. 開啟pyton IDE執行gui.py
2. input chrome driver path: 輸入chromedriver-win64.exe檔案路徑
3. input course code: 輸入想搜尋的課程代碼，點擊add
4. 點擊start search開始自動搜尋
5. available course: 顯示所有未額滿課程
6. 在search course點擊任意課程代碼，再點擊delete即可刪除搜尋課程
7. 當未額滿課程改變時，程式自動發出通知，所有可選課程自動複製到剪貼簿，輸入windows + v開啟
- note: 體育課程無法查詢各系人數限制, 及各系選課人數
   

