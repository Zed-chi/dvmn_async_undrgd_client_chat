# import logging
import asyncio
import aiofiles
from datetime import datetime
import configargparse


def get_args():
    p = configargparse.ArgParser(
        default_config_files=[
            "./config.txt",
        ]
    )
    p.add(
        "--host", required=True, help="host address"
    )  # this option can be set in a config file because it starts with '--'
    p.add("--port", required=True, help="port of the host")
    p.add("--log_path", required=True, help="history log path")
    return p.parse_args()


async def tcp_echo_client(args):
    reader, _ = await asyncio.open_connection(args.host, args.port)

    while True:
        data = await reader.readline()
        message = data.decode("utf-8")
        now = datetime.now().strftime("[%d.%m.%y %H:%M]")
        async with aiofiles.open(
            args.log_path, mode="a", encoding="utf-8"
        ) as f:
            await f.write(f"{now} {message}")
        print(f"{now} {message.strip()}")


if __name__ == "__main__":
    args = get_args()
    try:
        asyncio.run(tcp_echo_client(args))
    except KeyboardInterrupt:
        print("Client disconnected")
    except Exception as e:
        print(e)
