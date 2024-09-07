import asyncio
import random

from fastapi import FastAPI
from faststream.nats import JStream, DeliverPolicy
from faststream.nats.fastapi import NatsRouter, Logger
from app.models import Property, Target


router = NatsRouter(
    "nats://localhost:4222",
    schema_url="/asyncapi",
    include_in_schema=True,
)

version = "0.1.0"
title = "My FastStream service"
description = "Description of my FastStream service"

app = FastAPI(title=title, version=version, description=description)
stream = JStream(name="cdc-stream")

to_changes = router.publisher(
    "changes",
    description="Produces a message on greetings after receiving a meesage on names",
)


@router.subscriber(
    "properties",
    description="Consumes messages from names topic and produces messages to greetings topic",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
)
async def on_properties(msg: Property, logger: Logger) -> None:
    property = f"Delivering {msg.property_id}"
    logger.info(property)
    target = Target(message=msg)
    await router.broker.publish(target, subject="changes")


# @router.after_startup
# async def publish_names() -> None:
#     async def _publish_names() -> None:
#         names = [
#             "Ana",
#             "Mario",
#             "Pedro",
#             "João",
#             "Gustavo",
#             "Joana",
#             "Mariana",
#             "Juliana",
#         ]
#         while True:
#             name = random.choice(names)  # nosec


#             await router.broker.publish(Name(name=name), subject="names")



#             await asyncio.sleep(2)

#     asyncio.create_task(_publish_names())

app.include_router(router)
