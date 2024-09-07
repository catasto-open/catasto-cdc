import pytest
from faststream.nats import TestNatsBroker

from app.cdc import Property, Target, on_properties, router


@router.subscriber("changes")
async def on_changes(msg: Target) -> None:
    pass


@pytest.mark.asyncio
async def test_on_properties():
    async with TestNatsBroker(router):
        property = Property(
            identificativo_immobile=1,
            data_aggiornamento=datetime.now(),
            tipo_immobile=PropertyTypeEnum.F,
            identificativo_operazione=ChangeTypeEnum.accorpamento,
        )
        await router.broker.publish(property.model_dump(by_alias=True), "properties")
        on_properties.mock.assert_called_with(property.model_dump(by_alias=True))
        on_changes.mock.assert_called_with(Target(message=property).model_dump(by_alias=True))
