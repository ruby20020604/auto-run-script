import subprocess
import asyncio
from telegram import Bot

# Telegram Bot 配置
token = '8011582671:AAFS55JRsSEcBEh7xmys_mQYCoB-MocNDGs'
chat_id = '-494647345'

async def send_to_telegram(message):
    """非同步地發送訊息到 Telegram"""
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message)

def main():
    # 非阻塞地啟動 Chrome 瀏覽器
    chrome_command = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--remote-debugging-port=9222",
        "--user-data-dir=/tmp/chrome_dev"
    ]
    subprocess.Popen(chrome_command)

    # 啟動 1106.py 並監聽輸出
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

if __name__ == "__main__":
    main()
