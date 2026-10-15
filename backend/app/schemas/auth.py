from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    email: str
    password: str
    username: str


class LoginRequest(BaseModel):
    email: str
    password: str


class VerifyEmailRequest(BaseModel):
    email: str
    otp_code: str = Field(pattern=r"^\d{6}$")


class ResendVerificationRequest(BaseModel):
    email: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    email: str
    otp_code: str = Field(pattern=r"^\d{6}$")
    new_password: str


class MessageResponse(BaseModel):
    message: str


class SignupResponse(BaseModel):
    message: str
    email: str


class UserSummary(BaseModel):
    id: int
    email: str
    username: str
    is_verified: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserSummary
