# Issue 3.6: Implement call_agent_simulator Function (POST)

## Description
Create a Python function (e.g., call_agent_simulator) that accepts action_key, data_payload, and optional task_id. This function should use the requests library to send a POST request containing this data as a JSON payload to a new endpoint on the local Agent Simulator (e.g., http://localhost:5001/interact). Handle the basic response (expecting JSON).

## Acceptance Criteria
- Function exists and can be called after an interaction
- Successfully sends a POST request with the correct action key, collected data, and task ID (if present) to the simulator's /interact endpoint URL
- Returns parsed JSON response or None on error

## Estimate
Medium

## Dependencies
- Issue 3.5

## Execution Steps
1. Ensure requests is imported: `import requests`
2. Define the function, potentially in a separate api_client.py or within app.py:
```python
import requests
import streamlit as st # For st.secrets, st.error, st.spinner
import json

SIMULATOR_URL = st.secrets.get("SIMULATOR_URL", "http://localhost:5001") # Example: Get URL from secrets or default

def call_agent_simulator(action_key, data_payload, task_id):
    """Sends interaction data to the simulator and returns the new UI spec."""
    interact_url = f"{SIMULATOR_URL}/interact"
    # user_id will be added in Sprint 5
    payload = {
        "action_key": action_key,
        "data": data_payload,
        "task_id": task_id,
        "user_id": st.session_state.get("user_info", {}).get("email", "anonymous_poc_user") # Placeholder user
    }
    headers = {"Content-Type": "application/json"}
    new_ui_spec_response = None

    try:
        # Spinner added in Sprint 6, basic call here
        response = requests.post(interact_url, headers=headers, json=payload, timeout=10)
        response.raise_for_status() # Check for HTTP errors
        new_ui_spec_response = response.json() # Expecting JSON like {"status": "success", "view_config": [...]}

    except requests.exceptions.Timeout:
        st.error("Simulator timed out.") # Basic error handling for now
    except requests.exceptions.ConnectionError:
        st.error("Connection error: Cannot reach the simulator.")
    except requests.exceptions.RequestException as e:
        st.error(f"Simulator API Error: {e}")
    except json.JSONDecodeError:
         st.error("Received invalid JSON response from simulator.")
    except Exception as e:
         st.error(f"An unexpected error occurred during API call: {e}")

    return new_ui_spec_response # Returns dict or None
```

3. Integrate the call within the if triggered_action_key: block:
```python
if triggered_action_key:
    # ... (data collection logic from Issue 3.5) ...
    st.write(f"DEBUG: Calling simulator for action '{triggered_action_key}'")
    api_response = call_agent_simulator(triggered_action_key, data_payload, st.session_state.get("task_id"))

    if api_response and api_response.get("status") == "success":
         new_spec = api_response.get("view_config")
         st.session_state.current_ui_spec = new_spec
         # Optional: st.rerun() if immediate refresh needed
    elif api_response: # Handle structured errors if simulator sends them
         st.error(f"Agent Simulator Error: {api_response.get('message', 'Unknown error')}")
    # else: call_agent_simulator already displayed an error
```

4. Run the app and simulator. Click a button. Verify the POST request is made (check simulator logs) and the UI potentially updates based on the simulator's fixed response.
