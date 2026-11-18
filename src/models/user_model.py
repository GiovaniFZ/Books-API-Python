from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=1)
    
class AuthSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)
