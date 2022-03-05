import asyncio
import sys


async def main():
    reader, writer = await asyncio.open_connection('164.67.100.235', 10391)
    writer.write(f'{sys.argv[1]}\n'.encode())
    data = await reader.readline()
    print('Received: {}'.format(data.decode()))
    writer.close()
if __name__ == '__main__':
    asyncio.run(main())
