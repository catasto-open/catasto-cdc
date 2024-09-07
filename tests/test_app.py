import pytest
from datetime import datetime
from faststream.nats import TestNatsBroker

from app.cdc import router, on_properties
from app.models import Property, Target, PropertyTypeEnum, ChangeTypeEnum


@router.subscriber("changes")
async def on_changes(msg: Target) -> None:
    pass


@pytest.mark.asyncio
async def test_on_properties():
    async with TestNatsBroker(router.broker) as br:
        property = Property(
            identificativo_immobile=1,
            data_aggiornamento=datetime.now(),
            tipo_immobile=PropertyTypeEnum.F,
            identificativo_operazione=ChangeTypeEnum.accorpamento,
        )
        await br.publish(property, "properties", stream="cdc-stream")
        # on_properties.mock.assert_called_with(property.model_dump(by_alias=True))
        # on_changes.mock.assert_called_with(Target(message=property).model_dump(by_alias=True))
