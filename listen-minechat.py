import asyncio
from datetime import datetime

import aiofiles
import configargparse


def get_args():
    p = configargparse.ArgParser(
        default_config_files=[
            "./listener_config.txt",
        ],
    )
    p.add(
        "--host",
        required=False,
        help="host address",
        default="minechat.dvmn.org",
    )
    p.add("--port", required=False, help="port of sender client", default=5000)
    p.add(
        "--log_path",
        required=False,
        help="sender log path",
        default="./listener.log",
    )

    return p.parse_args()


async def tcp_echo_client(args):
    reader, _ = await asyncio.open_connection(args.host, args.port)

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


if __name__ == "__main__":
    args = get_args()
    try:
        asyncio.run(tcp_echo_client(args))
    except KeyboardInterrupt:
        print("Client disconnected")
