import asyncio
from datetime import datetime

import nats

from app.models import ChangeTypeEnum, Property, PropertyTypeEnum


async def main():
    br = await nats.connect("nats://localhost:4222")
    try:
        # Create JetStream context.
        js = br.jetstream()
        property = Property(
            property_id=1,
            changed_date=datetime.now(),
            property_type=PropertyTypeEnum.F,
            operation_id=ChangeTypeEnum.accorpamento,
        )
        # Persist messages on 'properties'.
        await js.add_stream(name="CATASTO", subjects=["CATASTO.changed"])
        ack = await js.publish(
            "CATASTO.changed",
            property.model_dump_json(by_alias=True).encode(),
        )
        print(ack)
        await br.close()
    except:
        raise


asyncio.run(main())
