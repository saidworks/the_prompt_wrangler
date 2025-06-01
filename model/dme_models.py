from typing import Optional
from pydantic import BaseModel, Field

class DMEBaseModel(BaseModel):
    """ Base Model for DME """
    ordering_provider: str = Field(max_length=256, min_length=1)

class CPAPMaskOrder(DMEBaseModel):
    device: str = Field(description="Type of device (e.g., 'CPAP' equipment)")
    mask_type: Optional[str] = Field(description="Specific type of mask used in the order")
    add_ons: Optional[list[str]] = Field(description="Additional components like humidifier")
    qualifier: Optional[str] = Field(description="Condition or measurement that requires this device (e.g., 'AHI > 20')")

class OxygenConcentratorOrder(DMEBaseModel):
    device: str = Field(description="Type of device (e.g., 'portable oxygen concentrator' equipment)")
    diagnosis: Optional[str] = Field(description="Medical condition for which the device is ordered")
    SpO2: Optional[str] = Field(description="SpO2 level measured on room air, if relevant")
    usage: Optional[list[str]] = Field(description="Scenarios in which the device is needed (e.g., 'exertion', 'sleep')")

class WheelchairOrder(DMEBaseModel):
    device: str = Field(description="Type of device (e.g., 'manual wheelchair' equipment)")
    type: Optional[str] = Field(description="Specific type of wheelchair, if applicable")
    features: Optional[list[str]] = Field(description="Additional features like elevating leg rests")
    diagnosis: Optional[str] = Field(description="Medical condition for which the device is ordered")
    mobility_status: Optional[str] = Field(description="Mobility status of the patient (e.g., 'non-ambulatory')")

class NebulizerOrder(DMEBaseModel):
    device: str = Field(description="Type of device (e.g., 'nebulizer' equipment)")
    accessories: Optional[list[str]] = Field(description="Additional components like mouthpiece and tubing")
    diagnosis: Optional[str] = Field(description="Medical condition for which the device is ordered")

class HospitalBedOrder(DMEBaseModel):
    device: str = Field(description="Type of device (e.g., 'hospital bed' equipment)")
    features: Optional[list[str]] = Field(description="Additional features like trapeze bar and side rails")
    diagnosis: Optional[str] = Field(description="Medical condition for which the device is ordered")
    mobility_status: Optional[str] = Field(description="Mobility status of the patient (e.g., 'non-ambulatory')")
    ordering_provider: str = Field(description="Physician who ordered the device")

class CPAPSuppliesOrder(DMEBaseModel):
    product: str = Field(description="Type of supplies requested (e.g., 'CPAP supplies'")
    components: Optional[list[str]] = Field(description="Specific components included in the request")
    compliance_status: Optional[str] = Field(description="Compliance status of the patient with current treatment")
