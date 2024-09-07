import asyncio
from nats.aio.client import Client as NATS
from nats.errors import TimeoutError


async def main():
    nc = NATS()

    # Connect to the NATS server
    await nc.connect("nats://localhost:4222")
    print("Connected to NATS server")

    # Create a JetStream context
    js = nc.jetstream()

    # Ensure the stream exists (if not created by FastStream)
    await js.add_stream(name="cdc-stream", subjects=["properties"])

    # Subscribe to the subject using JetStream with a durable name
    async def message_handler(msg):
        print(f"Received a message: {msg.data.decode()}")
        await msg.ack()  # Acknowledge message receipt

    try:
        await js.subscribe("*", durable="durable-consumer", cb=message_handler)
        print("Subscribed to the 'cdc-stream' subject with JetStream")

        # Keep the client running to listen for messages
        while True:
            await asyncio.sleep(1)

    except TimeoutError:
        print("Request timed out")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await nc.close()

if __name__ == "__main__":
    asyncio.run(main())
