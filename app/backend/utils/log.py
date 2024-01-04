import os
import json
from datetime import datetime


LOG_DIR = "logs/"

REQUEST = "REQUEST"
RESPONSE = "RESPONSE"


def log(msg, type):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"########## {current_time} {type} {msg}")

    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    log_file = now.strftime("%Y-%m-%d") + ".txt"
    with open(LOG_DIR + "log-" + log_file, "a") as f:
        f.write(f"########## {current_time} {type} {msg}\n")


def net_log(msg, type):
    data = json.dumps(msg)
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    log_file = now.strftime("%Y-%m-%d") + ".txt"
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    with open(LOG_DIR + "net-" + log_file, "a") as f:
        f.write(f"########## {current_time} {type} {data}\n")
