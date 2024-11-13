import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import pandas as pd
import os
import time
import subprocess

# 設定 Chrome 選項
options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("debuggerAddress", "localhost:9222")

# 使用 undetected_chromedriver
driver = uc.Chrome(options=options)

try:
    # 打開目標網頁
    driver.get('https://platform.openai.com/settings/organization/usage')
    #time.sleep(2)  # 等待頁面完全加載
    # 點擊登入按鈕
    login_button_xpath = '//*[@id="root"]/div[1]/div[1]/div[2]/div/button'
    login_button = WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.XPATH, login_button_xpath))
)
    login_button.click()



# 輸入 Google 帳號
    account_xpath = '//*[@id="email-input"]'
    account = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, account_xpath))
)
    account.clear()
    account.send_keys("yunyunw40@gmail.com")


# 點擊 "下一步" 按鈕
    next_button_xpath = '/html/body/div/main/section/div[2]/button'  # 修正變數名稱
    next_button = WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.XPATH, next_button_xpath))
)
    driver.execute_script("arguments[0].click();", next_button)


# 輸入密碼
    password_xpath = '//*[@id="password"]'
    password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, password_xpath))
)
    password.clear()
    password.send_keys("ruby20020604")


# 點擊 "繼續" 按鈕
    continue_button_xpath = '//*[@id="auth0-widget"]/main/section/div/div/div/form/div[2]/button'  # 修正變數名稱
    continue_button = WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.XPATH, continue_button_xpath))
)
    driver.execute_script("arguments[0].click();", continue_button)



    c_button_xpath = '//*[@id="root"]/div[1]/div[1]/div[2]/div'  # 修正變數名稱
    c_button = WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.XPATH, c_button_xpath))
)
    driver.execute_script("arguments[0].click();", c_button)
    # export按鈕
    quick_xpath = '//*[@id="root"]/div[1]/main/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/button'
    quick_button = WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.XPATH, quick_xpath))
    )
    driver.execute_script("arguments[0].click();", quick_button)

    yesterday = datetime.now() - timedelta(1)
    yesterday_str = yesterday.strftime('%d/%m/%Y')
    today = datetime.now()
    today_str = today.strftime('%d/%m/%Y')

    # 輸入start date
    sd_xpath = '//*[@id="root"]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[1]/div/input'
    sd = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, sd_xpath))
    )
    sd.click()
    for _ in range(len(sd.get_attribute("value"))):
        sd.send_keys(Keys.BACKSPACE)
    sd.send_keys(yesterday_str)
    #sd.send_keys("04/11/2024")
    
    # 輸入end date
    ed_xpath = '//*[@id="root"]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/input'
    ed = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, ed_xpath))
    )
    ed.clear()
    ed.click()
    for _ in range(len(ed.get_attribute("value"))):
        ed.send_keys(Keys.BACKSPACE)
    ed.send_keys(today_str)
    #ed.send_keys("05/11/2024")

    # 點擊確認按鈕
    order_xpath = '//*[@id="root"]/div[2]/div/div[2]/div/div[2]/div/div[2]/div[4]/div/button[1]'
    order_button = WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.XPATH, order_xpath))
    )
    order_button.click()

    # 設定檔案路徑
    start_date = yesterday.strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')
    #file_name = f"cost-2024-11-04-2024-11-05.csv"
    file_name = f"cost-{start_date}-{end_date}.csv"
    file_path = f'/opt/render/project/src/{file_name}'

    # 等待檔案下載完成
    max_wait_time = 30  # 最長等待30秒
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > max_wait_time:
            print("檔案下載超時")
            break
        time.sleep(1)

    # 處理數據
    if os.path.exists(file_path):
        time.sleep(2)  # 確保檔案寫入完成
        df = pd.read_csv(file_path)
        df_selected = df[['name', 'cost_in_major', 'date']]
        
        for index, row in df_selected.iterrows():
            print(f"{row['name']:10} {row['cost_in_major']:10.6f}    {row['date']:60}")
    
        pd.set_option('display.float_format', '{:.6f}'.format)
        total = df['cost_in_major'].sum()

        # 顯示內容
        #print(df_selected)
        print(f'total: {total}')

        # 刪除檔案
        os.remove(file_path)

except Exception as e:
    print(f"發生錯誤: {str(e)}")

finally:
    # 關閉瀏覽器
    driver.quit()
    # 關閉 Chrome
    chrome_close_command = [
        "osascript", "-e",
        'tell application "Google Chrome" to quit'
    ]
    subprocess.run(chrome_close_command)
