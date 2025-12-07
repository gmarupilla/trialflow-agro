"""
Data schema definitions for trialflow-agro.
"""

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


REQUIRED_COLUMNS = [
    "field_id",
    "farm_id",
    "region",
    "year",
    "product",
    "yield",
]

OPTIONAL_COLUMNS = [
    "treatment",
    "variety",
    "soil_class",
    "lat",
    "lon",
]


class TrialRow(BaseModel):
    """
    Pydantic model for a single row of trial data.

    This is primarily used for spot-check validation of the
    dataset (ensuring basic type consistency).
    """

    field_id: str
    farm_id: str
    region: str
    year: int
    product: str
    yield_: float = Field(alias="yield")

    treatment: Optional[str] = None
    variety: Optional[str] = None
    soil_class: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
    )
