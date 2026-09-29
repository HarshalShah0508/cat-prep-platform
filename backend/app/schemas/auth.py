from pydantic import BaseModel


class SignupRequest(BaseModel):
    email: str
    password: str
    username: str


class LoginRequest(BaseModel):
    email: str
    password: str


class UserSummary(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserSummary
