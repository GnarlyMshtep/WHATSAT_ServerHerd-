import asyncio
import sys


async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', sys.argv[1])
    writer.write(f'{sys.argv[2]}\n'.encode())
    writer.write_eof()
    data = await reader.read()
    print('Received: {}'.format(data.decode()))
    writer.close()

if __name__ == '__main__':
    asyncio.run(main())
