"""
Voice Agent:
- Voice call agent using Groq (Whisper STT + Llama3 LLM)
- Simple tool protocol: model outputs either:
    SAY: <assistant message>
  or CALL: <tool_name> {json_args}
- Mock tools: check_coverage, get_available_slots, book_appointment
- Conversation memory + end-of-call summary

Author:
- Name: Minh, Le Duc
- Email: minh.leduc.0210@gmail.com
- Github: https://github.com/MinLee0210
"""
