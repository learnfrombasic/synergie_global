from pydantic import BaseModel, Field


class CustomerDetail(BaseModel):
    name: str
    address: str
    phone: str
    email: str = Field(default="", description="Customer's email")
    service: str


class ConfirmAvailabitiy(BaseModel):
    is_availability: bool
    reasons: str


class ConversationNote(BaseModel):
    greeting: str
    customer_detail: CustomerDetail
    confirm_availablity: ConfirmAvailabitiy
    appointment_time: str
    confirmation: str
