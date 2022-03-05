import asyncio
from email.policy import default
from os import system
import sys


def parse_args():
    """
    parses command line arguments to either exit the program or return server_name, server_port
    """
    if len(sys.argv) <= 1 or len(sys.argv) >= 3:
        print('You must provide the server\'s name! The options are Juzang, Bernard, Jaquez, Johnson, or Clark. Please type one of the following as an argument and try again. Please do not include additional args. \n Exiting...')
        exit(1)
    else:
        arg1 = sys.argv[1]
        match arg1:
            case ('1' | "Juzang"):
                return "Juzang", 10391
            case ('2' | "Bernard"):
                return "Bernard", 10392
            case ('3' | "Jaquez"):
                return "Jaquez", 10393
            case ('4' | "Johnson"):
                return "Johnson", 10394
            case ('5' | "Clark"):
                return "Clark", 10395

        print(f'Unfortuntly the argument {arg1} you provided is not valid. Remember, the only valid options are Juzang, Bernard, Jaquez, Johnson, or Clark. Please type one of the following as an argument and try again. \n Exiting...')
        exit(1)


class Server:
    async def __init__(self):
        self.name, self.port_num = parse_args()
        self.server = await asyncio.start_server(self.handle_connection, host='164.67.100.235', port=self.port_num)
        await self.server.serve_forever()

    async def handle_connection(self, reader, writer):
        data = await reader.readline()
        name = data.decode()
        greeting = "Zepplin does rock, " + name
        writer.write(greeting.encode())
        await writer.drain()
        writer.close()


if __name__ == '__main__':
    asyncio.run(Server())
