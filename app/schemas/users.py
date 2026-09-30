from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    player_name: str
    password: str


class CreateUserResponse(BaseModel):
    email: EmailStr
    player_name: str

    model_config = ConfigDict(from_attributes=True)

class LoginUser(BaseModel):
    email: EmailStr
    password: str   

class LoginUserResponse(BaseModel):
    email: EmailStr
    player_name: str
    access_token: str
    token_type: str
    