# synergie_global
AI Engineer Test at SynergieGlobal


## Overview

Voice Agent:
- Voice call agent using Groq (Whisper STT + Llama3 LLM)
- Simple tool protocol: model outputs either:
    SAY: <assistant message>
  or CALL: <tool_name> {json_args}
- Mock tools: check_coverage, get_available_slots, book_appointment
- Conversation memory + end-of-call summary


## Usage

1. Create environment

```bash
uv venv
source .venv/bin/activate
uv sync
```

2. Install dependencies

```bash
sudo apt install portaudio19-dev python3-pyaudio   
```

3. Run the script

```bash
python -m src
```

## Contributors

- Minh, Le Duc (https://github.com/MinLee0210)