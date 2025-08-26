from pydantic import BaseModel, EmailStr

# ✅ Input model when creating/registering a new user
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str 

# ✅ Input model when logging in
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# ✅ Response model (never return raw password!)
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str

    class Config:
        orm_mode = True