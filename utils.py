import configargparse


def get_args():
    p = configargparse.ArgParser(
        default_config_files=[
            "./config.txt",
        ],
    )
    p.add("--host", required=True, help="host address")
    p.add("--sender_port", required=True, help="port of sender client")
    p.add("--token", help="token", required=False)
    p.add("--port", required=True, help="port of the viewer client")
    p.add("--sender_log_path", required=False, help="sender log path")
    p.add("--history_path", required=False, help="history log path")
    p.add("--name", required=False, help="name for registration")

    return p.parse_args()
