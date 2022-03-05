import datetime
import time


class Logger:
    def __init__(self) -> None:
        self.server_name = "NOT_YET_SET"
        self.count = 1

    def set_server_name(self, name: str):
        self.server_name = name
        with open(f'./logs/{self.server_name}', "a") as f:
            # to seperate between sessions
            f.write(
                f'\n--------------------------------------\n{time.time(), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            # log a seperator from the last sessions

    def log_request(self, req_str, timestamp):
        with open(f'./logs/{self.server_name}', "a") as f:
            f.write(f'{self.count}. REQ, {timestamp}, {req_str.strip()}\n')
        self.count += 1

    def log_response(self, res_str, timestamp, to):
        with open(f'./logs/{self.server_name}', "a") as f:
            f.write(
                f'{self.count}. RES, {timestamp}, to->({to}), {res_str.strip()}\n')
        self.count += 1

    def log_connection_err(self, to_server_name, ex, timestamp):
        with open(f'./logs/{self.server_name}', "a") as f:
            f.write(
                f'{self.count}. CFL, {timestamp}, to: {to_server_name}, due {ex}\n')
        self.count += 1
