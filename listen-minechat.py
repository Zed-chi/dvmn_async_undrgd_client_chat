import asyncio
from datetime import datetime

import aiofiles

import configargparse


CONFIG_FILEPATH = "./listener_config.cfg"


def get_args():
    parser = configargparse.ArgParser(
        default_config_files=[
            CONFIG_FILEPATH,
        ],
    )
    parser.add(
        "--host",
        required=False,
        help="host address",
        default="minechat.dvmn.org",
    )
    parser.add("--port", required=False, help="port of sender client", default=5000)
    parser.add(
        "--log_path",
        required=False,
        help="sender log path",
        default="./listener.log",
    )

    return parser.parse_args()


async def listen_chat(args):
    reader, writer = await asyncio.open_connection(args.host, args.port)

    try:
        while True:
            data = await reader.readline()
            message = data.decode("utf-8")
            now = datetime.now().strftime("[%d.%m.%y %H:%M]")
            if "history_path" in args:
                async with aiofiles.open(
                    args.history_path,
                    mode="a",
                    encoding="utf-8",
                ) as f:
                    await f.write(f"{now} {message}")
            print(f"{now} {message.strip()}")
    finally:
        writer.close()
        await writer.wait_closed()
    


if __name__ == "__main__":
    args = get_args()
    try:
        asyncio.run(listen_chat(args))
    except KeyboardInterrupt:
        print("Client disconnected")
