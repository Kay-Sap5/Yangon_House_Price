from pydantic import BaseModel , Field , field_validator 
from typing import Annotated , Literal 

from src.logging.logger import logging
from src.exception.exception import CustomException
import sys
import pandas as pd

city_list = [
    'others', 'ahlon', 'bahan', 'dagon myothit (north)', 'dagon myothit (south)', 
    'dawbon', 'hlaing', 'kamaryut', 'lanmadaw', 'mayangone', 'okkalappa north', 
    'okkalappa south', 'sanchaung', 'tamwe', 'thaketa', 'thanlyin', 'thingangkuun', 'yankin'
]

type_list = [
    'Apartment','Condo','House'
]

class InputValidation_Model(BaseModel):
    city : Annotated[str , Literal[tuple(city_list)]]
    type : Annotated[str , Literal[tuple(type_list)]]
    bed_room : int = Field(... , ge = 1)
    bath_room: float = Field(... , ge = 1)
    floor : int = Field(... , ge = 1)
    ft_square : float = Field(... , ge = 300)

    @field_validator('city')
    @classmethod
    def validate(cls , inp):
        if inp not in city_list:
            raise ValueError('City Must Be in the City_List')
        return inp
    
    @field_validator('type')
    @classmethod
    def validate_type(cls , inp):
        if inp not in type_list:
            raise ValueError('Type Must Be in the Type_List')
        return inp





