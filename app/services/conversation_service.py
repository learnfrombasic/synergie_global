import json
import re
from typing import Any, Dict, List, Optional

from groq import Groq

from ..configs.settings import settings
from ..models.conversation import (ConversationContext, ConversationState,
                                   Message, MessageRole)
from ..prompts.conversation import get_initial_messages, get_system_prompt


class ConversationService:
    """Manages the conversation flow and state."""

    def __init__(self, groq_client: Groq):
        self.client = groq_client
        self.messages = get_initial_messages()
        self.context = ConversationContext()
        self.state = ConversationState.GREETING

        # Update system prompt based on initial state
        self._update_system_prompt()

    def process_user_input(self, user_input: str) -> str:
        """Process user input and return assistant's response."""
        # Add user message to history
        self._add_message(Message(role=MessageRole.USER, content=user_input))

        try:
            # Get model response
            response = self._get_model_response()

            # Handle tool calls if present
            if response.tool_calls:
                return self._handle_tool_calls(response)

            # Add assistant message to history
            self._add_message(
                Message(role=MessageRole.ASSISTANT, content=response.content or "")
            )

            # Update conversation state based on response
            self._update_conversation_state(response.content)

            return response.content

        except Exception as e:
            error_msg = f"I'm sorry, I encountered an error: {str(e)}"
            self._add_message(Message(role=MessageRole.ASSISTANT, content=error_msg))
            self.state = ConversationState.ERROR
            return error_msg

    def _get_model_response(self):
        """Get response from the language model."""
        response = self.client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[msg.dict() for msg in self.messages],
            temperature=0.2,
        )
        return response.choices[0].message

    def _handle_tool_calls(self, response) -> str:
        """Handle tool calls from the model."""
        tool_calls = response.tool_calls
        if not tool_calls:
            return ""

        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            try:
                args = json.loads(tool_call.function.arguments)
                result = self._execute_tool(tool_name, args)
                results.append(f"{tool_name} result: {result}")

                # Add tool result to messages
                self._add_message(
                    Message(
                        role=MessageRole.TOOL,
                        content=json.dumps(result),
                        tool_call_id=tool_call.id,
                        name=tool_name,
                    )
                )

            except Exception as e:
                error_msg = f"Error executing {tool_name}: {str(e)}"
                results.append(error_msg)
                self._add_message(
                    Message(
                        role=MessageRole.TOOL,
                        content=json.dumps({"error": error_msg}),
                        tool_call_id=tool_call.id,
                        name=tool_name,
                    )
                )

        # Get model's response to tool results
        return self._get_model_response().content

    def _execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name with the given arguments."""
        # This would be connected to actual tool implementations
        # For now, return a mock response
        return {
            "status": "success",
            "tool": tool_name,
            "args": args,
            "result": f"Mock result for {tool_name}",
        }

    def _update_conversation_state(self, response: str):
        """Update conversation state based on the assistant's response."""
        # Simple state machine to update conversation state
        # This is a simplified version - you'd want to make this more sophisticated
        if "goodbye" in response.lower() or "thank you" in response.lower():
            self.state = ConversationState.CLOSING
        # Add more state transition logic here

        # Update system prompt based on new state
        self._update_system_prompt()

    def _update_system_prompt(self):
        """Update the system prompt based on current state and context."""
        # Update the system message in messages
        system_prompt = get_system_prompt(self.state, self.context.to_dict())

        # Find and update the system message
        for msg in self.messages:
            if msg.role == MessageRole.SYSTEM:
                msg.content = system_prompt
                break
        else:
            # Add system message if not found
            self.messages.insert(
                0, Message(role=MessageRole.SYSTEM, content=system_prompt)
            )

    def _add_message(self, message: Message):
        """Add a message to the conversation history."""
        self.messages.append(message)

        # Keep conversation history to a reasonable size
        if len(self.messages) > 20:  # Keep last 20 messages
            # Keep system message and last 19 messages
            system_msg = next(
                (m for m in self.messages if m.role == MessageRole.SYSTEM), None
            )
            self.messages = (
                [system_msg] + self.messages[-19:]
                if system_msg
                else self.messages[-20:]
            )
