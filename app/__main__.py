"""
Main entry point for the Jacobs Plumbing Voice Assistant.

This application provides a voice interface for customers to book plumbing appointments
using Groq's LLM for natural language understanding and response generation.
"""

import logging
import os
import sys
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq

# Local imports
from app.configs.settings import settings
from app.services.audio_service import AudioService
from app.services.conversation_service import ConversationService


def initialize_services():
    """Initialize all required services."""
    try:
        # Initialize Groq client
        client = Groq(api_key=settings.GROQ_API_KEY)

        # Initialize audio service
        audio_service = AudioService()

        # Initialize conversation service
        conversation_service = ConversationService(groq_client=client)

        return client, audio_service, conversation_service

    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise


def get_user_input(audio_service: AudioService, voice_mode: bool = True) -> str:
    """Get input from the user, either via voice or text."""
    if voice_mode:
        if settings.PUSH_TO_TALK:
            input("\n🎙️ Press Enter to record… ")

        # Record audio
        audio_data = audio_service.record_audio(settings.RECORDING_DURATION)

        # Convert speech to text
        try:
            # For now, we'll just return a placeholder since we don't have STT set up
            # In a real implementation, you would use Groq's STT here
            user_text = input("👤 (Type your message since STT is not implemented): ")
            logger.info(f"User said: {user_text}")
            return user_text
        except Exception as e:
            logger.error(f"Error in speech-to-text: {e}")
            return ""
    else:
        return input("👤 You: ").strip()


def main():
    """Main application loop."""
    print("\n" + "=" * 50)
    print("🔧 Jacobs Plumbing - Voice Assistant")
    print("=" * 50)
    print("Type 'quit' or 'exit' to end the conversation.\n")

    try:
        # Initialize services
        client, audio_service, conversation = initialize_services()

        print(
            "\n🤖 Assistant: Hello! Welcome to Jacob's Plumbing. How can I assist you today?"
        )

        while True:
            # Get user input
            user_input = get_user_input(audio_service, settings.VOICE_MODE)

            # Check for exit conditions
            if not user_input or user_input.lower() in [
                "quit",
                "exit",
                "bye",
                "goodbye",
            ]:
                print(
                    "\n🤖 Assistant: Thank you for calling Jacob's Plumbing. Have a great day!"
                )
                break

            # Process user input and get response
            try:
                response = conversation.process_user_input(user_input)
                print(f"\n🤖 Assistant: {response}")

                # Convert response to speech if in voice mode
                if settings.VOICE_MODE:
                    audio_service.text_to_speech(response)

            except Exception as e:
                error_msg = f"I'm sorry, I encountered an error: {str(e)}"
                logger.error(f"Error in conversation: {e}", exc_info=True)
                print(f"\n❌ {error_msg}")

                if settings.VOICE_MODE:
                    audio_service.text_to_speech(error_msg)

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        print("\n❌ A critical error occurred. Please check the logs for details.")
    finally:
        print("\nThank you for using Jacob's Plumbing Assistant!")


if __name__ == "__main__":
    main()
