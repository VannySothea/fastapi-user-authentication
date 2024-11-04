from app.responses.base import BaseResponse
from pydantic import EmailStr
from datetime import datetime
from typing import Union


class AllDevicesResponse(BaseResponse):
    device_id: str
    device_name: str
    created_at: Union[str, None, datetime] = None
    last_used_at: Union[str, None, datetime] = None
