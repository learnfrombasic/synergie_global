from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(BaseModel):
    """Represents a single message in the conversation."""

    role: MessageRole
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None


class ConversationState(str, Enum):
    INITIAL = "initial"
    COLLECTING_INFO = "collecting_info"
    CHECKING_COVERAGE = "checking_coverage"
    OFFERING_SLOTS = "offering_slots"
    BOOKING = "booking"
    CONFIRMATION = "confirmation"
    COMPLETED = "completed"
    ERROR = "error"


class ConversationContext(BaseModel):
    """Tracks the state and context of an ongoing conversation."""

    state: ConversationState = ConversationState.INITIAL
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    service_address: Optional[str] = None
    service_request: Optional[str] = None
    available_slots: List[str] = []
    selected_slot: Optional[str] = None
    confirmation_id: Optional[str] = None
    metadata: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert the context to a dictionary for serialization."""
        return {
            "state": self.state.value,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "customer_email": self.customer_email,
            "service_address": self.service_address,
            "service_request": self.service_request,
            "available_slots": self.available_slots,
            "selected_slot": self.selected_slot,
            "confirmation_id": self.confirmation_id,
            "metadata": self.metadata,
        }
