import datetime
import time


class Logger:
    def __init__(self) -> None:
        self.server_name = "NOT_YET_SET"

    def set_server_name(self, name: str):
        self.server_name = name
        with open(f'./logs/{self.server_name}', "a") as f:
            # to seperate between sessions
            f.write(
                f'\n--------------------------------------\n{time.time(), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            # log a seperator from the last sessions

    def log_request(self, req_str, timestamp):
        with open(f'./logs/{self.server_name}', "a") as f:
            f.write(f'REQ, {timestamp}, {req_str}\n')
