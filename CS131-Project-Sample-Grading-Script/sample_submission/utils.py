import json
import aiohttp
import logger
import time  # for debuf
import os

u_logger = logger.Logger()
u_logger.set_server_name('util')
u_logger.log_debug('intiated ulogger', time.time())


def read_api_key(logger):
    #u_logger.log_debug(f'in readpai_key:{os.getcwd()}', time.time())
    try:
        with open(f'{os.path.dirname(os.path.realpath(__file__))}/places_api_key.secret') as f:
            x = f.readline()
        #u_logger.log_debug(f'api_key is {x}', time.time())
        return x
    except IOError as e:
        logger.log_debug(
            f'Error is {e}\n but probably just couldn\'t open places_api_key.txt, the servers will fail. \nExiting...', time.time())
        exit(1)


def parse_loc_for_http(client_loc: str):
    ret = "" if client_loc[0] == "+" else "-"
    if client_loc[1:].find('+') >= 0:
        ls = client_loc[1:].split('+')
        ret += ls[0] + "%2C" + ls[1]
    else:
        ls = client_loc[1:].split('-')
        ret += ls[0] + "%2C-" + ls[1]
    return ret


async def make_place_req(api_key, client_loc, client_parsed_radius, client_num_item: int):
    parsed_loc = parse_loc_for_http(client_loc)
    req_str = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={parsed_loc}&radius={client_parsed_radius}&key={api_key}'
    print(req_str)
    async with aiohttp.ClientSession() as session:
        async with session.get(req_str) as resp:
            res = await resp.json()
            res['results'] = res['results'][0:client_num_item]
            return json.dumps(res, indent=2)
