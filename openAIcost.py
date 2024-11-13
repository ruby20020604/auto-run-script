import subprocess
import asyncio
from telegram import Bot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Telegram Bot 配置
token = '8011582671:AAFS55JRsSEcBEh7xmys_mQYCoB-MocNDGs'
chat_id = '-4576563147'

async def send_to_telegram(message):
    """非同步地發送訊息到 Telegram"""
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message)

def main():
    # 設定 Chrome 選項
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")


    # 使用 Selenium WebDriver 啟動 Chrome
    driver = webdriver.Chrome(options=options)

    port = os.getenv("PORT", 8000)

    # 在指定的 port 上啟動 Flask 應用程式
    app.run(host="0.0.0.0", port=port)

    # 非阻塞地啟動 1106.py
    python_command = ["python3", "openAIcost_run.py"]
    process = subprocess.Popen(python_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    loop = asyncio.get_event_loop()
    buffer = []  # 用於存儲多行輸出

    try:
        # 實時監聽 1106.py 的輸出
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break

            if output.strip():  # 如果有內容，加入緩衝區
                buffer.append(output.strip())
            else:  # 空行表示輸出結束，合併並發送
                if buffer:
                    message = "\n".join(buffer)  # 合併多行
                    print(message)  # 在終端打印
                    loop.run_until_complete(send_to_telegram(message))
                    buffer.clear()  # 清空緩衝區

        # 處理剩餘的緩衝內容
        if buffer:
            message = "\n".join(buffer)
            print(message)
            loop.run_until_complete(send_to_telegram(message))

        # 處理錯誤輸出
        stderr = process.stderr.read()
        if stderr:
            print("Error:", stderr)
            loop.run_until_complete(send_to_telegram(f"Error: {stderr.strip()}"))
    finally:
        loop.close()
        driver.quit()

if __name__ == "__main__":
    main()
