import asyncio
import datetime
from http import client  # to conduct server activities
import sys  # to get args
import time  # to time when requests came

server_name = "NULL"  # this will be set as soon as we know


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


async def main(port_num):
    # I think host is right?
    server = await asyncio.start_server(handle_connection, host='164.67.100.235', port=port_num)
    await server.serve_forever()


async def propagate_IAMAT_to_herd():
    pass

# we will need to read and then write to others


async def handle_connection(reader, writer):
    recieved_timestamp = time.time()
    data = await reader.readline()
    dec_str = data.decode()
    dec_lst = dec_str.split()  # two sources of truth, not  super good

    if len(dec_lst) != 4:
        writer.write(("? " + dec_str).encode())
    else:  # message is of proper length, meaning that it is proper
        if dec_lst[0] == "IAMAT":  # write back for an IAMAT response
            client_name = dec_lst[1]
            client_loc = dec_lst[2]
            client_sent_timestamp = dec_lst[3]
            # check that float conversion works
            await propagate_IAMAT_to_herd()  # we choose to await the propagation, to avoid teh case where the client gets a response from server, and queries another server before the IAMAT has been prpagated to him
            writer.write(
                (f'AT {server_name} {recieved_timestamp-float(client_sent_timestamp)} {client_name} {client_loc} {client_sent_timestamp}').encode())
        elif dec_lst[0] == "WHATSAT":
            pass
        else:  # some other invalid request
            writer.write(("? " + dec_str).encode())

    await writer.drain()
    writer.close()

if __name__ == '__main__':
    server_name, port_num = parse_args()
    asyncio.run(main(port_num))
