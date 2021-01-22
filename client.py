import asyncio
import aiofiles
from datetime import datetime
#import logging


HOST = "minechat.dvmn.org"
PORT = 5000
LOG_NAME = "history.log"

async def tcp_echo_client():
    reader, _ = await asyncio.open_connection(
        HOST, PORT)    

    while True:
        data = await reader.readline()
        message = data.decode("utf-8")
        now = datetime.now().strftime("[%d.%m.%y %H:%M]")
        async with aiofiles.open(LOG_NAME, mode='a', encoding="utf-8") as f:
            await f.write(f"{now} {message}")
        print(f"{now} {message.strip()}")

if __name__ == "__main__":
    try:
        asyncio.run(tcp_echo_client())
    except KeyboardInterrupt:
        print("Client disconnected")
    except Exception as e:
        print(e)

