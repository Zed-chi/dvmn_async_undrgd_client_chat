import asyncio
import logging
import json

import aiofiles
from utils import get_args


async def tcp_echo_client(args):
    reader, writer = await asyncio.open_connection(args.host, args.port)

    welcome = await reader.readline()
    log(f"{welcome.decode()}")

    if "token" in args:
        await authorize(args.token, reader, writer)
    else:
        await register(get_name(args), reader, writer)

    try:
        while True:
            message = sanitize(input("Send: "))
            await submit_message(message, reader, writer)
    finally:
        writer.close()
        await writer.wait_closed()


async def submit_message(message, reader, writer):
    if not message:
        return
    writer.write(f"{message}\n\n".encode())
    await writer.drain()
    data = await reader.readline()
    log(f"{data.decode()}")


def get_name(args):
    if "name" in args:
        return args.name
    while True:
        name = sanitize(input("Type a name to register: "))
        if name:
            return name


async def authorize(token, reader, writer):
    writer.write(f"{token}\n".encode())
    await writer.drain()

    response_info = (await reader.readline()).decode().strip()
    log(f"res is {response_info}")
    if not json.loads(response_info):
        raise ValueError("Invalid token. Check or register new.")


async def register(name, reader, writer):
    writer.write("\n".encode())
    await writer.drain()

    data = await reader.readline()
    log(f"{data.decode()}")

    writer.write(f"{name}\n\n".encode())
    await writer.drain()

    info_json = (await reader.readline()).decode().strip()
    user_info_dict = json.loads(info_json)
    await save_token(user_info_dict)

    writer.write("\n".encode())
    await writer.drain()

    data = await reader.readline()
    log(f"{data.decode()}")


async def save_token(user_info_dict):
    async with aiofiles.open("./config.txt", mode="a", encoding="utf-8") as f:
        token = user_info_dict["account_hash"]
        await f.write(f"\ntoken={token}")


def sanitize(string):
    newstr = string
    for ch in ["\\n", "\\t", "\\r", "\\f", "\\b", "\\a", "\\"]:
        newstr = newstr.replace(ch, "")
    return newstr


def log(message, args):
    if "sender_log_path" in args:
        logging.info(message)


if __name__ == "__main__":
    args = get_args()
    if "sender_log_path" in args:
        logging.basicConfig(
            level=logging.INFO,
            filename=args.sender_log_path,
            format="%(levelname)s:sender:%(message)s",
        )

    try:
        asyncio.run(tcp_echo_client(args))
    except KeyboardInterrupt:
        logging.info("Client disconnected")
    except Exception as e:
        logging.info(e)
