import asyncio

class Server:
    def __init__(self):
        self.clients = []

    async def handle_client(self, reader, writer):
        self.clients.append(writer)
        try:
            while True:
                data = await reader.read(200)
                message = data.decode().strip()
                if not message:
                    break
                print(f"Client: {message}")
                await self.broadcast(message)
        except asyncio.CancelledError:
            pass
        finally:
            print("Client disconnected")
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def broadcast(self, message):
        if self.clients:
            print(f"Broadcast: {message}")
            tasks = [client.write(message.encode()) for client in self.clients]
            await asyncio.gather(*tasks)

async def main():
    server = Server()
    server_address = ('localhost', 3005)

    chat_server = await asyncio.start_server(
        server.handle_client, *server_address
    )

    print(f"Server started on {server_address}")

    async with chat_server:
        await chat_server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())