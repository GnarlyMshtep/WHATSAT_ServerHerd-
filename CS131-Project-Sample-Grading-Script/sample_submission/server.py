import asyncio  # to conduct server activities
import datetime  # DEBUG
import sys  # to get args
import time  # to time when requests came
from logger import Logger
import utils

server_name = "NULL"  # this will be set as soon as we know
client_infos = {}
server_to_port = {
    "Juzang": 10391,
    "Bernard": 10392,
    "Jaquez": 10393,
    "Johnson": 10394,
    "Clark": 10395,
}
servers_can_communic_with = {
    "Juzang": ["Clark", "Johnson", "Bernard"],
    "Bernard": ["Juzang", "Jaquez", "Johnson"],
    "Jaquez":  ["Clark", "Bernard"],
    "Johnson": ["Bernard", "Juzang"],
    "Clark": ["Jaquez", "Juzang"],
}
all_srv_names = ["Juzang", "Bernard", "Jaquez", "Johnson", "Clark"]

logger = Logger()


def possibly_update_client_infos(client_name, client_timestamp, client_loc, orig_recieving_server):
    """if there is more recent information about that client stored, don't update. Else, do."""
    if client_name in client_infos.keys():
        if float(client_infos[client_name][0]) < float(client_timestamp):

            client_infos[client_name] = (
                client_timestamp, client_loc, orig_recieving_server)
            # print('client_update happening in',
            #      server_name, 'for', client_name, client_infos)
    else:
        client_infos[client_name] = (
            client_timestamp, client_loc, orig_recieving_server)
        # print('client_update happening in',
        #      server_name, 'for', client_name, client_infos)


async def main(port_num):
    # I think host is right?
    #logger.log_debug(f'In main!', time.time())
    server = await asyncio.start_server(handle_connection, host='127.0.0.1', port=port_num)
    await server.serve_forever()


async def send_PROPAG_CMSG(to_server_name, from_server, send_ls, client_name, client_loc, client_sent_timestamp):
    """
    from_server = dec_lst[1]
    sent_ls = dec_lst[2]
    client_name = dec_lst[3]
    client_timestamp = dec_lst[4]
    client_loc = dec_lst[5]
    """
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', server_to_port[to_server_name])
    except Exception as ex:
        logger.log_connection_err(to_server_name, ex, time.time())
        return
    logger.log_open_connection(to_server_name, time.time())

    res_str = f'PROPAG_CMSG {from_server} {send_ls} {client_name} {client_sent_timestamp} {client_loc}'
    writer.write((res_str + '\n').encode())
    await writer.drain()
    logger.log_response(res_str, time.time(), f'SRV:{to_server_name}')

    writer.close()
    logger.log_close_connection(to_server_name, time.time())


async def propagate_IAMAT_to_herd(send_ls, client_name, client_loc, client_sent_timestamp):
    """
        if we got here, it means that send_ls has been checked and we should propagate -- !checking does not occur here

        so far, gets called in first send

        A flooding "algorithm" particularly optimised for our scenrio
        (we can compute optimal sending given that any single player has recieved a message)
        recalling that any given server may be off, and we must transmit the packet whenever possible
    """
    for neighbor_server_name in servers_can_communic_with[server_name]:
        # no need to send to someone who already had it
        if neighbor_server_name not in send_ls.split(','):
            await send_PROPAG_CMSG(neighbor_server_name, server_name, send_ls, client_name, client_loc, client_sent_timestamp)


async def handle_connection(reader: asyncio.StreamReader, writer):
    # logger.log_debug(
    #    'I recieved a request! currently in handle_connection', time.time())
    recieved_timestamp = time.time()
    data = await reader.read()  # works if client adds an EOF, gurenteed by @257
    dec_str = data.decode()
    logger.log_request(dec_str, recieved_timestamp)
    dec_lst = dec_str.strip().split()  # two sources of truth, not super good

    # if the length is not 4 (reg clinet message) and not (srver propagate message)
    if len(dec_lst) != 4 and not (len(dec_lst) == 6 and dec_lst[0] == "PROPAG_CMSG"):
        writer.write(("? " + dec_str).encode())
        logger.log_response("? " + dec_str, time.time(), '?:?')

    else:  # message is of proper length, meaning that it is proper. the following could be a case table, but then default gets akward
        if dec_lst[0] == "IAMAT":  # write back for an IAMAT response
            client_name = dec_lst[1]
            client_loc = dec_lst[2]
            client_sent_timestamp = dec_lst[3]
            # check that float conversion works
            possibly_update_client_infos(
                client_name, client_sent_timestamp, client_loc, server_name)
            # we choose to await the propagation, to avoid teh case where the client gets a response from server, and queries another server before the IAMAT has been prpagated to him
            # we always prop since this is the first request
            await propagate_IAMAT_to_herd(server_name, client_name, client_loc, client_sent_timestamp)
            res_str = f'AT {client_infos[client_name][2]} {recieved_timestamp-float(client_sent_timestamp)} {client_name} {client_loc} {client_sent_timestamp}'
            writer.write(res_str.encode())
            logger.log_response(res_str, time.time(), f'CLI:{client_name}')

        elif dec_lst[0] == "WHATSAT":
            client_name = dec_lst[1]
            client_radius = str(float(dec_lst[2])*1000)  # mul to get to meters
            client_item_lim = dec_lst[3]

            if client_name not in client_infos.keys():
                print(
                    f"{client_name}'s location has not been recorded! \n Exiting...")
                exit(1)  # !Not sure what to do

            res_str = f'AT {client_infos[client_name][2]} {recieved_timestamp-float(client_infos[client_name][0])} {client_name} {client_infos[client_name][1]} {client_infos[client_name][0]}'

            api_res_str = await utils.make_place_req(
                api_key, client_infos[client_name][1], client_radius, int(client_item_lim))
            full_res_str = res_str+"\n"+api_res_str+"\n"
            writer.write(full_res_str.encode())
            logger.log_response(full_res_str, time.time(),
                                f'CLI:{client_name}')

        elif dec_lst[0] == "PROPAG_CMSG":
            # get some vars to be explicit
            send_ls = dec_lst[2]
            client_name = dec_lst[3]
            client_timestamp = dec_lst[4]
            client_loc = dec_lst[5]

            # update self record
            possibly_update_client_infos(
                client_name, client_timestamp, client_loc, send_ls.split(',')[0])

            # propagate forward
            if server_name not in send_ls.split(','):
                await propagate_IAMAT_to_herd(
                    send_ls+","+server_name, client_name, client_loc, client_timestamp)

        else:  # some other invalid request, not sure if those are even allowed
            writer.write(("? " + dec_str).encode())
            logger.log_response("? " + dec_str, time.time(), "?:?")

    await writer.drain()
    writer.close()


def parse_init_args():
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
                return "Juzang", server_to_port["Juzang"]
            case ('2' | "Bernard"):
                return "Bernard", server_to_port["Bernard"]
            case ('3' | "Jaquez"):
                return "Jaquez", server_to_port["Jaquez"]
            case ('4' | "Johnson"):
                return "Johnson", server_to_port["Johnson"]
            case ('5' | "Clark"):
                return "Clark", server_to_port["Clark"]

        print(f'Unfortuntly the argument {arg1} you provided is not valid. Remember, the only valid options are Juzang, Bernard, Jaquez, Johnson, or Clark. Please type one of the following as an argument and try again. \n Exiting...')
        exit(1)


if __name__ == '__main__':
    server_name, port_num = parse_init_args()
    logger.set_server_name(server_name)
    api_key = utils.read_api_key(logger)
    asyncio.run(main(port_num))
