import logging
import asyncio
import aiofiles
from utils import get_args
import json



async def tcp_echo_client(host, port, token=None):
    reader, writer = await asyncio.open_connection(host, port)

    welcome = await reader.readline()
    logging.info(f"{welcome.decode()}")

    if token:
        await sign_in(token, reader, writer)
    else:
        name = input("pick a name: ")
        await sign_up(name, reader, writer)

    try:
        while True:
            message = input("Send: ")
            writer.write(f"{message}\n\n".encode())
            await writer.drain()
            data = await reader.readline()
            logging.info(f"{data.decode()}")
    except:
        writer.close()
        await writer.wait_closed()


async def sign_in(token, r, w):
    w.write(f"{token}\n".encode())
    await w.drain()

    response_info = (await r.readline()).decode().strip()
    logging.info(f"res is {response_info}")
    if not json.loads(response_info):
        raise ValueError("Invalid token. Check or register new.")


async def sign_up(name, r, w):
    w.write(f"\n".encode())
    await w.drain()

    data = await r.readline()
    logging.info(f"{data.decode()}")

    w.write(f"{name}\n\n".encode())
    await w.drain()

    info_json = (await r.readline()).decode().strip()
    user_info_dict = json.loads(info_json)
    await save_token(user_info_dict)

    w.write(f"\n".encode())
    await w.drain()

    data = await r.readline()
    logging.info(f"{data.decode()}")


async def save_token(user_info_dict):
    async with aiofiles.open("./config.txt", mode="a", encoding="utf-8") as f:
        token = user_info_dict["account_hash"]
        await f.write(f"\ntoken={token}")


if __name__ == "__main__":
    args = get_args()
    if args.debug:
        logging.basicConfig(level=logging.INFO, filename="sender.log", format="%(levelname)s:sender:%(message)s")
    else:
        logging.basicConfig(level=logging.WARNING, filename="sender.log", format="%(levelname)s:sender:%(message)s")    

    try:
        asyncio.run(
            tcp_echo_client(
                args.host,
                args.sender_port,
                args.token
            )
        )
    except KeyboardInterrupt:
        logging.info("Client disconnected")
    except Exception as e:
        logging.info(e)
