import asyncio
from datetime import datetime
from faststream.nats import NatsBroker
from nats.errors import NoServersError
from app.models import ChangeTypeEnum, Property, PropertyTypeEnum


broker = NatsBroker("nats://localhost:4222")

async def main():
    async with NatsBroker() as br:
        try:
            property = Property(
                property_id=1,
                changed_date=datetime.now(),
                property_type=PropertyTypeEnum.F,
                operation_id=ChangeTypeEnum.accorpamento,
            )
            await br.publish(property.model_dump(by_alias=True), subject="properties", stream="cdc-stream")
        except:
            raise

asyncio.run(main())
