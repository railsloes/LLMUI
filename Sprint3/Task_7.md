# Issue 3.7: Update Agent Simulator (POST Endpoint)

## Description
Add the /interact POST endpoint to the Agent Simulator script (Flask/FastAPI). This endpoint should receive the JSON payload, print/log the received action_key, data, and task_id for verification. For this sprint, it should return a fixed, predefined next UI spec (e.g., always return CHAT_SPEC as JSON) regardless of the input, just to complete the loop.

## Acceptance Criteria
- Simulator's /interact endpoint runs and receives POST data
- Logs the received data correctly to the console
- Returns a valid, predefined UI spec JSON wrapped in the status structure ({"status": "success", "view_config": CHAT_SPEC})

## Estimate
Small

## Dependencies
- Issue 3.6 (needs endpoint to call)

## Execution Steps
1. Open the Agent Simulator script (agent_simulator.py)
2. Add the /interact route handler:
```python
# Assume CHAT_SPEC dictionary is defined here
CHAT_SPEC = [
    {"type": "markdown", "text": "Chat view shown after interaction."},
    {"type": "chat_interface", "key": "agent_chat"}
]

@app.route('/interact', methods=['POST'])
def post_interact():
    payload = request.get_json()
    print("SIMULATOR: Received POST /interact with payload:") # Log
    print(json.dumps(payload, indent=2))

    # For Sprint 3, always return a fixed spec upon successful interaction
    action_key = payload.get("action_key")
    if action_key: # Basic check that we got something
        # In future, logic here would depend on action_key/data/state
        response_data = {"status": "success", "view_config": CHAT_SPEC}
    else:
        response_data = {"status": "error", "message": "Missing action_key"}

    return jsonify(response_data)
```

3. Update imports at the top of the file if needed:
```python
from flask import Flask, request, jsonify
import json
```

4. Restart the simulator
5. Run the Streamlit app, trigger an interaction (e.g., click button in a form view)
6. Verify the simulator logs the received payload
7. Verify the Streamlit UI updates to show the CHAT_SPEC content
