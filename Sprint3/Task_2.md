# Issue 3.2: Update Agent Simulator for task_id

## Description
Modify the agent_simulator.py file to read the task_id from the query parameters when the `/get_spec/<version>` endpoint is called. For now, just print the received task_id to the console.

## Acceptance Criteria
- Simulator running locally returns different predefined JSON specs when called with different task_id query parameters via curl or browser

## Estimate
Small

## Dependencies
- Completed Step 1 (Basic Simulator)

## Execution Steps
1. In agent_simulator.py, locate the get_specific_spec function that handles the `/get_spec/<version>` route.
```python
from flask import Flask, request, jsonify

# Assume TEXT_SPEC, FORM_SPEC, CHAT_SPEC dictionaries are defined here
# (Copy them from the Streamlit app's definitions for consistency)
TEXT_SPEC = [{"type": "markdown", "text": "Default Text View (No Task ID)"}]
FORM_SPEC = [{"type": "markdown", "text": "Form View (Task ID='form')"}, {"type": "text_input", "label": "Task Input", "key": "task_form_input"}]
# ... define other specs ...

app = Flask(__name__)

@app.route('/get_spec', methods=['GET'])
def get_ui_spec():
    task_id = request.args.get('task_id')
    print(f"SIMULATOR: Received GET /get_spec request with task_id='{task_id}'") # Log

    if task_id == 'form':
        spec_to_return = FORM_SPEC
    # Add elif for other specific task_ids if needed
    else:
        spec_to_return = TEXT_SPEC # Default

    # For MVP, always succeed if spec found
    response_data = {"status": "success", "view_config": spec_to_return}
    return jsonify(response_data)
```

3. Run the simulator
4. Test using curl or browser:
   - http://localhost:5001/get_spec (should return TEXT_SPEC)
   - http://localhost:5001/get_spec?task_id=form (should return FORM_SPEC)
   - http://localhost:5001/get_spec?task_id=other (should return TEXT_SPEC)
