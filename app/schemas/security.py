from pydantic import BaseModel, EmailStr


class DeviceRemove(BaseModel):
    device_id: str