from typing import Union
from pydantic import BaseModel
from model.dme_models import *


class Output(BaseModel):
    """Output model to structures llm response"""
    final_output : Union[CPAPSuppliesOrder, CPAPMaskOrder, HospitalBedOrder, WheelchairOrder, NebulizerOrder, OxygenConcentratorOrder]




