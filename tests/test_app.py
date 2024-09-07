import pytest
from faststream.nats import TestNatsBroker

from app.cdc import Greeting, Name, on_names, router


@router.subscriber("greetings")
async def on_greetings(msg: Greeting) -> None:
    pass


@pytest.mark.asyncio
async def test_on_names():
    async with TestNatsBroker(router):
        await router.broker.publish(Name(name="John"), "names")
        on_names.mock.assert_called_with(dict(Name(name="John")))
        on_greetings.mock.assert_called_with(dict(Greeting(greeting="hello John")))
