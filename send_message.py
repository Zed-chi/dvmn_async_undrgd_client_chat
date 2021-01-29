import asyncio
import json
import logging

import aiofiles

import configargparse

CONFIG_FILEPATH = "./sender_config.cfg"


def get_args():
    p = configargparse.ArgParser(
        default_config_files=[
            CONFIG_FILEPATH,
        ],
    )
    p.add(
        "--host",
        required=False,
        help="host address",
        default="minechat.dvmn.org",
    )
    p.add("--port", required=False, help="port of sender client", default=5050)
    p.add("--token", help="token", required=False)
    p.add(
        "--log_path",
        required=False,
        help="sender log path",
        default="./sender.log",
    )
    p.add(
        "--name", required=False, help="name for registration", default="user"
    )
    p.add("--message", required=True, help="message to send")

    return p.parse_args()


async def send_message(args):
    reader, writer = await asyncio.open_connection(args.host, args.port)

    log((await reader.readline()).decode())

    if args.token:
        await authorize(args.token, reader, writer)
    else:
        await register(get_name(args), reader, writer)

    try:
        message = sanitize(args.message)
        await submit_message(message, reader, writer)
    finally:
        writer.close()
        await writer.wait_closed()


async def submit_message(message, reader, writer):
    if not message:
        return
    writer.write(f"{message}\n\n".encode())
    await writer.drain()

    log((await reader.readline()).decode())


def get_name(args):
    if args.name:
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

    log((await reader.readline()).decode())

    writer.write(f"{name}\n\n".encode())
    await writer.drain()

    info_json = (await reader.readline()).decode().strip()
    user_info_dict = json.loads(info_json)
    await save_token(user_info_dict)

    writer.write("\n".encode())
    await writer.drain()

    log((await reader.readline()).decode())


async def save_token(user_info_dict):
    async with aiofiles.open(CONFIG_FILEPATH, mode="a", encoding="utf-8") as f:
        token = user_info_dict["account_hash"]
        await f.write(f"\ntoken={token}")


def sanitize(string):
    newstr = string
    for ch in ["\\n", "\\t", "\\r", "\\f", "\\b", "\\a", "\\"]:
        newstr = newstr.replace(ch, "")
    return newstr


def log(message):
    logging.info(message)


if __name__ == "__main__":
    args = get_args()

    logging.basicConfig(
        level=logging.INFO,
        filename=args.log_path,
        format="%(levelname)s:sender:%(message)s",
    )

    try:
        asyncio.run(send_message(args))
    except KeyboardInterrupt:
        logging.info("Client disconnected")
    except ValueError:
        logging.warning("Invalid token. Check or register new.")
