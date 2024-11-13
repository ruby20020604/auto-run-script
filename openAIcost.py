import subprocess
import asyncio
from telegram import Bot

# Telegram Bot 配置
TOKEN = '8011582671:AAFS55JRsSEcBEh7xmys_mQYCoB-MocNDGs'
CHAT_ID = '-494647345'

async def send_to_telegram(message):
    """非同步地發送訊息到 Telegram"""
    try:
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"無法發送訊息到 Telegram: {e}")

async def read_process_output(process):
    """非同步地讀取子程序輸出"""
    buffer = []
    while True:
        line = await process.stdout.readline()
        if line == b"" and process.returncode is not None:
            break
        decoded_line = line.decode("utf-8").strip()
        if decoded_line:
            buffer.append(decoded_line)
        else:
            if buffer:
                message = "\n".join(buffer)
                print(message)  # 在終端打印
                await send_to_telegram(message)  # 發送到 Telegram
                buffer.clear()

    # 處理剩餘的緩衝內容
    if buffer:
        message = "\n".join(buffer)
        print(message)
        await send_to_telegram(message)

async def run_script():
    """執行主邏輯"""
    # 啟動 openAIcost_run.py 並監聽輸出
    python_command = ["python3", "/opt/render/project/src/openAIcost.py"]
    process = await asyncio.create_subprocess_exec(
        *python_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # 同時處理標準輸出和錯誤輸出
    await asyncio.gather(
        read_process_output(process),
        read_process_output(process)
    )

    # 處理錯誤輸出
    stderr = await process.stderr.read()
    if stderr:
        error_message = stderr.decode("utf-8").strip()
        print(f"Error: {error_message}")
        await send_to_telegram(f"Error: {error_message}")

def main():
    """執行主程序"""
    asyncio.run(run_script())

if __name__ == "__main__":
    main()
