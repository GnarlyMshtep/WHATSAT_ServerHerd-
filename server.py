import asyncio
from email.policy import default
from os import system
import sys


def parse_args():
    if len(sys.argv) <= 1:
        print('You must provide the server\'s name! The options are Juzang, Bernard, Jaquez, Johnson, or Clark. Please type one of the following as an argument and try again. \n Exiting...')
        exit(1)
    else:
        arg1 = sys.argv[1]
        match arg1:
            case ('1' | "Juzang"):
                return 10391
            case ('2' | "Juzang"):
                return 10392
            case ('3' | "Juzang"):
                return 10393
            case ('4' | "Juzang"):
                return 10394
            case ('5' | "Juzang"):
                return 10395

        print(f'Unfortuntly the argument {arg1} you provided is not valid. Remember, the only valid options are Juzang, Bernard, Jaquez, Johnson, or Clark. Please type one of the following as an argument and try again. \n Exiting...')
        exit(1)


async def main(port_num):
    # I think host is right?
    server = await asyncio.start_server(handle_connection, host='164.67.100.235', port=port_num)
    await server.serve_forever()


# we will need to read and then write to others
async def handle_connection(reader, writer):
    data = await reader.readline()
    name = data.decode()
    greeting = "Zepplin does rock, " + name
    writer.write(greeting.encode())
    await writer.drain()
    writer.close()
if __name__ == '__main__':
    port_num = parse_args()
    asyncio.run(main(port_num))
