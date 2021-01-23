# import logging
import asyncio

HOST = "minechat.dvmn.org"
PORT = 5050
TOKEN = "84e46b1a-5d99-11eb-8c47-0242ac110002"

async def tcp_echo_client():
    reader , writer = await asyncio.open_connection(HOST, PORT)
    try:
        data = await reader.readline()
        print(f'{data.decode()}')
        writer.write(f"{TOKEN}\n\n".encode())
        await writer.drain()
        info = await reader.readline()
        print(f'{info.decode()}')
        writer.write(f"\n\n".encode())
        await writer.drain()
        while True:
            message = input("Send: ")    
            writer.write(f"{message}\n\n".encode())
            await writer.drain()
            data = await reader.readline()
            print(f'{data.decode()}')
    except:
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":    
    try:
        asyncio.run(tcp_echo_client())
    except KeyboardInterrupt:
        print("Client disconnected")
    except Exception as e:
        print(e)
