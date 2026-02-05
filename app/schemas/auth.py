from pydantic import BaseModel, EmailStr, constr

class RegisterSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=72)

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str