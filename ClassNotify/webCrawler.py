# webCrawler.py
import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as webDriverWait
from selenium.webdriver.support import expected_conditions as EC
from win10toast import ToastNotifier
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PATH = "C:/program_Files/chromedriver-win32/chromedriver.exe"
url = 'https://querycourse.ntust.edu.tw/querycourse/#/'
classCode = ['FE1621702','FE1621703','PE111A022','PE113A022','PE114A022','PE115A022','PE127A022','PE139A022','TCG078301','TCG057301']
availableClass = []
driver = None
#print selenium version
print(webdriver.__version__)

def init():
    global driver
    driver = webdriver.Chrome(executable_path=PATH)
    driver.maximize_window()
    driver.get(url)

def getCurrentSelect(result):
    isGeneralEducation = False
    for j in range(0, len(result)):
        if(result[j].find('通識領域課程') != -1):
            isGeneralEducation = True
            break
        
    if(isGeneralEducation):
        return result[18].split('(')[0], isGeneralEducation
    else:
        return result[17].split('(')[0], isGeneralEducation
    
def getMaxSelect():
    moreInfo = driver.find_element_by_xpath("//*[contains(text(), 'more_horiz')]")
    moreInfo.click()
    webDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '本校加退選人數上限/新生第一學期初選人數上限：')]")))
    infoResult = moreInfo.find_element_by_xpath("//*[contains(text(), '本校加退選人數上限/新生第一學期初選人數上限：')]")
    
    while(len(infoResult.text.split('：')) < 2):
        infoResult = moreInfo.find_element_by_xpath("//*[contains(text(), '本校加退選人數上限/新生第一學期初選人數上限：')]")
        time.sleep(0.1)
    
    return infoResult.text.split('：')[1]

def sendNotify():
    if(len(availableClass) == 0):
        return

    notifyStr = ""

    for i in range(0, len(availableClass)):
        notifyStr += availableClass[i][0] + " " + availableClass[i][1] + '\n'

    toast = ToastNotifier()
    toast.show_toast("搶課通知", notifyStr, duration=0, threaded=True)

def printResult(result, resultIndex, currentSelect, maxSelect):
    print('name: ' + result[resultIndex])
    print('current select: ' + currentSelect)
    print('max select: ' + maxSelect)

def send_email(className, classCode):
    pass

def start_search(callback):
    global availableClass
    result = []

    while True:
        tempAvailableClass = []

        for i in range(0, len(classCode)):
            webDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label=課程代碼]")))
            search = driver.find_element_by_css_selector("[aria-label=課程代碼]")

            search.send_keys(classCode[i])
            time.sleep(0.3)
            search.send_keys(Keys.RETURN)
            webDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'more_horiz')]")))

            table = driver.find_element_by_class_name('v-datatable')
            result = table.text.split(' ')

            currentSelect, isGeneralEducation = getCurrentSelect(result)     
            maxSelect = getMaxSelect()

            resultIndex = 12
            if(isGeneralEducation):
                resultIndex = 13

            if(int(currentSelect) < int(maxSelect)):
                tempAvailableClass.append([classCode[i], result[resultIndex]])

            printResult(result, resultIndex, currentSelect, maxSelect)

            time.sleep(0.5)
            driver.refresh()
        
        if(availableClass != tempAvailableClass):
            availableClass = tempAvailableClass
            sendNotify()
            callback(availableClass)  # Update the GUI with the available classes

        time.sleep(random.randint(2, 10))

    driver.quit()

def setPath(path):
    global PATH
    if path != "":
        PATH = path
        init()

def setClassCode(code):
    global classCode
    classCode = code

