import configargparse
import json


def get_args():
    p = configargparse.ArgParser(
        default_config_files=[
            "./config.txt",
        ]
    )
    p.add("--debug", required=True, help="debug")
    p.add("--host", required=True, help="host address")    
    p.add("--sender_port", required=True, help="port address")    
    p.add("--token", help="token", required=False)
    p.add("--port", required=True, help="port of the host")
    p.add("--log_path", required=True, help="history log path")
    return p.parse_args()