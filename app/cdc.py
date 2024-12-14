from fastapi import FastAPI
from faststream.nats import DeliverPolicy, JStream
from faststream.nats.fastapi import Logger, NatsRouter

from app.config.app import configuration as cfg
from app.models import Property, Target

router = NatsRouter(
    cfg.NATS_SERVER_URL,
    schema_url="/asyncapi",
    include_in_schema=True,
)

version = "0.1.0"
title = "CDC FastStream service"
description = "Description of CDC FastStream service"

app = FastAPI(title=title, version=version, description=description)
stream = JStream(name=cfg.STREAM)

to_changes = router.publisher(
    cfg.NATS_NOTIFICATION_SUBJECT,
    description=f"\
    Produces a message on {cfg.NATS_NOTIFICATION_SUBJECT} \
    after receiving a message on {cfg.NATS_CATASTODB_SUBJECT}",
)


@router.subscriber(
    cfg.NATS_CATASTODB_SUBJECT,
    description=f"\
    Consumes messages from {cfg.NATS_CATASTODB_SUBJECT} \
    topic and produces messages to {cfg.NATS_NOTIFICATION_SUBJECT} topic",
    stream=stream,
    deliver_policy=DeliverPolicy.NEW,
)
async def on_properties(msg: Property, logger: Logger) -> None:
    property = f"Delivering {msg.property_id}"
    logger.info(property)
    target = Target(message=msg)
    await router.broker.publish(target, subject=f"{cfg.NATS_NOTIFICATION_SUBJECT}")


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
