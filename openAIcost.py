import asyncio
import os
from telegram import Bot

# Telegram Bot 配置
TOKEN = os.getenv("TELEGRAM_TOKEN", "你的Token")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "你的Chat ID")

async def send_to_telegram(message):
    """非同步地發送訊息到 Telegram"""
    try:
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"無法發送訊息到 Telegram: {e}")

async def read_process_output(process):
    """讀取子進程的輸出並發送到 Telegram"""
    try:
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            decoded_line = line.decode().strip()
            print(decoded_line)
            await send_to_telegram(decoded_line)
    except Exception as e:
        print(f"讀取輸出時出錯: {e}")

async def run_script():
    """執行主邏輯"""
    script_path = os.path.join(os.getenv("RENDER_ROOT", "/opt/render/project/src/"), "openAIcost_run.py")

    # 啟動子進程
    process = await asyncio.create_subprocess_exec(
        "python3", script_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # 使用單一協程處理 stdout
    await read_process_output(process)

    # 確保子進程執行完成
    await process.wait()

if __name__ == "__main__":
    asyncio.run(run_script())
