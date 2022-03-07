import datetime  # for humanreadable datetime at the begining of each eceution
import time     # for timestamp at the begining of each execution
import os       # for making the logs directory of it doesn't exist

we_at = os.path.dirname(os.path.realpath(__file__))


class Logger:
    def __init__(self) -> None:
        self.server_name = "NOT_YET_SET"
        self.count = 1
        if not os.path.exists(f'{we_at}/logs'):
            os.mkdir(f'{we_at}/logs')

    def set_server_name(self, name: str):
        self.server_name = name
        with open(f'{we_at}/logs/{self.server_name}', "a") as f:
            # to seperate between sessions
            f.write(
                f'\n--------------------------------------\n{time.time(), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            # log a seperator from the last sessions

    def log_request(self, req_str, timestamp=-99):
        with open(f'{we_at}/logs/{self.server_name}', "a") as f:
            f.write(f'{self.count}. REQ, {timestamp}, {req_str.strip()}\n')
        self.count += 1

    def log_response(self, res_str, timestamp, to):
        with open(f'{we_at}/logs/{self.server_name}', "a") as f:
            f.write(
                f'{self.count}. RES, {timestamp}, to->({to}), {res_str.strip()}\n')
        self.count += 1

    def log_open_connection(self, to_server_name, timestamp=-99):
        with open(f'{we_at}/logs/{self.server_name}', "a") as f:
            f.write(
                f'{self.count}. SOC, {timestamp}, to: {to_server_name}\n')
        self.count += 1

    def log_close_connection(self, to_server_name, timestamp=-99):
        with open(f'{we_at}/logs/{self.server_name}', "a") as f:
            f.write(
                f'{self.count}. SCC, {timestamp}, to: {to_server_name}\n')
        self.count += 1

    def log_connection_err(self, to_server_name, ex, timestamp=-99):
        with open(f'{we_at}/logs/{self.server_name}', "a") as f:
            f.write(
                f'{self.count}. CFL, {timestamp}, to: {to_server_name}, due {ex}\n')
        self.count += 1

    def log_debug(self, message, timestamp=-99):
        with open(f'{we_at}/logs/{self.server_name}', "a") as f:
            f.write(
                f'{self.count}. DBG, {timestamp}, {message}\n')
        self.count += 1
