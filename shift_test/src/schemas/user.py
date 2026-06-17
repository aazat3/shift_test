from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    is_administrator: bool


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

