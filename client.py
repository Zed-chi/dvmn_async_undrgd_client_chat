import asyncio

HOST = "minechat.dvmn.org"
PORT = 5000

async def tcp_echo_client():
    reader, _ = await asyncio.open_connection(
        HOST, PORT)    

    while True:
        data = await reader.readline()
        print(f'{data.decode()}')

if __name__ == "__main__":
    try:
        asyncio.run(tcp_echo_client())
    except:
        print("Client disconnected")

