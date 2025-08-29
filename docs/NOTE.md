# synergie_global
AI Engineer Test at SynergieGlobal

## Task Description


## 1. Analyze the Recording

* Listen to the provided call between **Nick (Jacobs Plumbing)** and **Steven Manley (customer)**.
* Note the **flow of the conversation**, including:

  * Greeting and introduction
  * Collecting customer details (name, address, phone, email, service request)
  * Confirming availability
  * Scheduling the appointment
  * Reconfirming the details with the customer
* Your analysis will help you mirror the same professional style in your AI assistant.

## 2. Create a Prompt for the AI

* Draft a **prompt (instruction set)** that guides the AI on **how to handle calls**.
* The prompt must ensure the AI:

  * Greets politely and professionally.
  * Asks for all required details (name, address, phone number, email, service request).
  * Confirms available service slots.
  * Books the appointment.
  * Confirms details back to the customer.
* Keep the language clear, concise, professional, and courteous.

## 3. Implement the Agentic AI (Python)

* Develop a **Python script** that implements a simple agentic AI.
* Requirements:

  * Use the prompt from Step 2.
  * Add **context handling** (so the AI remembers details already collected).
  * Add **tool calls** (mock functions for scheduling, checking availability, etc.).
  * Make it capable of running through a conversation like the recording.

## 4. Provide a Full Script (CSV)

* Recreate the **entire conversation** from the recording as if the AI handled it.
* Save it in **CSV format** with columns:

  ```
  Speaker, Dialogue
  ```
* Each row = one turn (e.g., AI asks, Caller responds).
* The flow should match the recording: greeting → info collection → appointment confirmation → closing.

## 5. (Optional) Additional Test Cases

* Create **extra scenarios** (e.g., unavailable time slots, different service request).
* Provide **short scripts** in the same CSV format to show your AI works in more than one case.

## Deliverables

1. **Prompt** (text file or section in your submission).
2. **AI Agent Python implementation** (source code).
3. **CSV Script** for the provided scenario.
4. *(Optional)* CSV scripts for extra test cases.
