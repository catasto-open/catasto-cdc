import pytest
from faststream.nats import TestNatsBroker

from catasto-cdc.application import Greeting, Name, broker, on_names


@broker.subscriber("greetings")
async def on_greetings(msg: Greeting) -> None:
    pass


@pytest.mark.asyncio
async def test_on_names():
    async with TestNatsBroker(broker):
        await broker.publish(Name(name="John"), "names")
        on_names.mock.assert_called_with(dict(Name(name="John")))
        on_greetings.mock.assert_called_with(dict(Greeting(greeting="hello John")))
