import io
import json
import os
import re
from typing import Any, Dict, List

import pyttsx3
from groq import Groq
from scipy.io.wavfile import write as wav_write
from langchain_groq import ChatGroq

from src.configs import settings
from src.cores import chat_groq, record_audio, stt_groq, tts_say
from src.tools import TOOLS, read_reprompts
from src.prompts import SYSTEM_PROMPT, INSTRUCTIONS
from src.schemas import ConversationNote
from src.commons import setup_logger

SLOTS_DB: Dict[str, List[str]] = {}
BOOKINGS: List[Dict[str, Any]] = []
CALL_RE = re.compile(r"^\s*CALL:\s*([a-zA-Z_][\w]*)\s*(\{.*\})\s*$", re.DOTALL)
SAY_RE = re.compile(r"^\s*SAY:\s*(.+)\s*$", re.DOTALL)

logger = setup_logger(settings.APP_NAME)

"""
NOTE: 
Context handling via history
"""

# Make system_prompt
reprompts = read_reprompts(file_path=str(settings.ROOT_DIR / "samples" / "dialog.xlsx"))
system_prompt = SYSTEM_PROMPT.format(
    owner=settings.APP_NAME,
    instructions=INSTRUCTIONS,
    dialog=str(reprompts),
)

print(system_prompt)
def new_history():
    return [{"role": "system", "content": system_prompt}]


def add_user(history, text):
    history.append({"role": "user", "content": text})


def add_assistant(history, text):
    history.append({"role": "assistant", "content": text})


def parse_action(text: str) -> Dict[str, Any]:
    """
    Returns:
      {"type": "call", "tool": str, "args": dict}
      or {"type": "say", "text": str}
      or {"type": "unknown", "raw": str}
    """
    m = CALL_RE.match(text)
    if m:
        tool = m.group(1).strip()
        arg_str = m.group(2).strip()
        try:
            args = json.loads(arg_str)
        except Exception:
            args = {"_raw_args": arg_str}
        return {"type": "call", "tool": tool, "args": args}

    m = SAY_RE.match(text)
    if m:
        return {"type": "say", "text": m.group(1).strip()}

    return {"type": "unknown", "raw": text}


def make_summary(history: List[Dict[str, str]]) -> str:
    llm = ChatGroq(model_name=settings.GROQ_MODEL_NAME)
    llm_evaluate_dialog = llm.bind_tools([ConversationNote])
    conversation_note = llm_evaluate_dialog.invoke(history)
    return conversation_note.tool_calls[0].get("args", {})


def main():

    client = Groq(api_key=settings.GROQ_API_KEY)
    history = new_history()

    # TTS engine
    tts = pyttsx3.init()
    tts.setProperty("rate", 175)

    logger.info("📞 Call started. Speak or type as the CUSTOMER.")
    logger.info("   Say 'bye' or 'thank you' to end.\n")

    while True:
        # === Get customer input (voice or typed) ===
        if settings.VOICE_MODE:
            if settings.PUSH_TO_TALK:
                input("🎙️ Press Enter to record… (3s)")
            audio = record_audio(3.0)
            # Save to wav buffer
            buf = io.BytesIO()
            wav_write(buf, settings.SAMPLE_RATE, audio)
            buf.seek(0)
            user_text = stt_groq(client, buf.getvalue())
            logger.debug(f"👤 Customer (STT): {user_text}")
        else:
            user_text = input("👤 Customer: ").strip()

        if not user_text:
            continue

        add_user(history, user_text)
        if any(
            x in user_text.lower() for x in ["bye", "goodbye", "thank you", "thanks"]
        ):
            break

        # === Ask model what to do (SAY or CALL) ===
        assistant_text = chat_groq(client, history)
        action = parse_action(assistant_text)

        # If model didn't follow protocol, nudge once
        if action["type"] == "unknown":
            nudge = (
                "Please follow the protocol strictly. Either:\n"
                "SAY: <message>\n"
                "or\nCALL: <tool_name> {json}"
            )
            add_assistant(history, nudge)
            logger.debug("🤖 AI (nudge):", nudge)
            if settings.VOICE_MODE:
                tts_say(tts, "Sorry, could you repeat that?")
            continue

        # === Handle tool calls until model says something ===
        tool_guard = 0
        while action["type"] == "call" and tool_guard < 4:
            tool_guard += 1
            tool_name = action["tool"]
            args = action["args"]
            fn = TOOLS.get(tool_name)
            if fn is None:
                tool_result = {"error": f"Unknown tool: {tool_name}"}
            else:
                # call tool safely
                try:
                    tool_result = fn(**args)
                except TypeError:
                    tool_result = {"error": f"Bad args for {tool_name}", "got": args}

            # Feed tool result back to the model as an assistant message (tool result)
            tool_msg = f"TOOL_RESULT {tool_name}: {json.dumps(tool_result, ensure_ascii=False)}"
            add_assistant(history, tool_msg)

            # Ask the model to continue (it may SAY or CALL again)
            assistant_text = chat_groq(client, history)
            action = parse_action(assistant_text)

        # === If SAY, speak to caller ===
        if action["type"] == "say":
            spoken = action["text"]
            add_assistant(history, f"SPOKEN: {spoken}")
            logger.debug("🤖 AI:", spoken)
            if settings.VOICE_MODE:
                tts_say(tts, spoken)
        else:
            # If we fall out without SAY, just print raw
            add_assistant(history, assistant_text)
            logger.debug("🤖 AI(raw):", assistant_text)

    # === End of call -> Summary ===
    logger.info("\n📝 Generating conversation note…\n")
    note = make_summary(history)
    logger.info(note)


if __name__ == "__main__":
    main()
