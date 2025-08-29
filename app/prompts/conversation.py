from enum import Enum
from typing import Any, Dict

from ..configs.settings import settings


class ConversationState(str, Enum):
    """Possible states of the conversation."""

    GREETING = "greeting"
    COLLECTING_INFO = "collecting_info"
    CHECKING_COVERAGE = "checking_coverage"
    OFFERING_SLOTS = "offering_slots"
    BOOKING = "booking"
    CONFIRMATION = "confirmation"
    CLOSING = "closing"
    ERROR = "error"


# System prompt templates
SYSTEM_PROMPTS = {
    ConversationState.GREETING: """
    You are a polite and professional AI assistant for {company_name}.
    Greet the caller warmly and introduce yourself.
    Ask how you can assist them today.
    """,
    ConversationState.COLLECTING_INFO: """
    Collect the following information from the caller:
    1. Full name
    2. Service address
    3. Phone number
    4. Email address
    5. Description of the plumbing service needed
    
    Ask for one piece of information at a time in a natural, conversational way.
    """,
    ConversationState.CHECKING_COVERAGE: """
    Check if the provided address is within the service area.
    Use the check_coverage tool with the address.
    If not covered, explain politely and suggest alternatives if available.
    """,
    ConversationState.OFFERING_SLOTS: """
    Present available time slots to the caller.
    Use the get_available_slots tool to get available times.
    Ask which time slot works best for them.
    """,
    ConversationState.BOOKING: """
    Finalize the appointment booking.
    Use the book_appointment tool with all collected information.
    Confirm all details with the caller before proceeding.
    """,
    ConversationState.CONFIRMATION: """
    Provide the caller with their booking confirmation details:
    - Date and time
    - Service address
    - Service description
    - Confirmation number
    - Any preparation instructions
    """,
    ConversationState.CLOSING: """
    Thank the caller for choosing {company_name}.
    Let them know what to expect next.
    Provide contact information for any questions.
    End the call politely.
    """,
    ConversationState.ERROR: """
    An error occurred during the conversation.
    Apologize to the caller and try to resolve the issue.
    If the issue persists, offer alternative contact methods.
    """,
}


def get_system_prompt(state: ConversationState, context: Dict[str, Any] = None) -> str:
    """Get the appropriate system prompt for the current conversation state."""
    context = context or {}
    prompt = SYSTEM_PROMPTS.get(state, "")

    # Add company name and other dynamic values
    context.setdefault("company_name", "Jacob's Plumbing")

    return prompt.format(**context)


def get_initial_messages() -> list:
    """Get the initial conversation messages with system prompt."""
    return [
        {
            "role": "system",
            "content": """You are a helpful AI assistant for Jacob's Plumbing. Be polite, professional, and concise. """
            """Follow the conversation flow and use the provided tools when needed.""",
        }
    ]


def get_tool_prompt(tool_name: str) -> str:
    """Get instructions for using a specific tool."""
    tool_prompts = {
        "check_coverage": "Check if the address is within our service area.",
        "get_available_slots": "Get available appointment slots for the given address.",
        "book_appointment": "Book an appointment with the provided details.",
    }
    return tool_prompts.get(tool_name, "")


def format_appointment_confirmation(booking_details: Dict[str, Any]) -> str:
    """Format the appointment confirmation message."""
    return f"""
    Thank you for booking with Jacob's Plumbing!
    
    Appointment Details:
    - Date & Time: {booking_details.get("date_time", "Not specified")}
    - Service: {booking_details.get("service", "Plumbing service")}
    - Address: {booking_details.get("address", "Not specified")}
    - Confirmation #: {booking_details.get("confirmation_id", "Pending")}
    
    A plumber will arrive within the scheduled time window. 
    Please call us at (555) 123-4567 if you have any questions.
    """
