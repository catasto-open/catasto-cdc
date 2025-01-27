from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class PropertyTypeEnum(Enum):
    T = "Terreni"
    F = "Fabbricati"


class ChangeTypeEnum(Enum):
    frazionamento = "FRAZIONAMENTO"
    accorpamento = "ACCORPAMENTO"


class Property(BaseModel):
    property_id: Annotated[
        int,
        Field(
            ...,
            description="Identificativo dell'immobile",
            alias="identificativo_immobile",
        ),
    ]
    changed_date: Annotated[
        datetime,
        Field(
            ...,
            description="Data di aggiornamento",
            alias="data_aggiornamento",
        ),
    ]
    property_type: Annotated[
        PropertyTypeEnum,
        Field(
            ...,
            description="Tipologia dell'immobile",
            alias="tipo_immobile",
        ),
    ]
    operation_id: Annotated[
        ChangeTypeEnum,
        Field(
            ...,
            description="Identificativo dell'operazione",
            alias="identificativo_operazione",
        ),
    ]

    model_config = ConfigDict(populate_by_name=True)


class Target(BaseModel):
    message: Property
