# Issue 3.5: Implement Basic Data Collection

## Description
When an action_key is detected (Issue 3.3), implement logic to iterate through the current UI spec again, find known input elements (text_input, selectbox for MVP), and collect their current values from st.session_state using their respective keys. Store these in a data_payload dictionary.

## Acceptance Criteria
- When a button defined in a form spec is clicked, the data_payload dictionary correctly contains the current values from the text_input elements defined in that same spec

## Estimate
Medium

## Dependencies
- Issue 3.3

## Execution Steps
1. In app.py, locate the if triggered_action_key: block after the detection loop
2. Add the data collection logic:
```python
if triggered_action_key:
    st.write(f"DEBUG: Action '{triggered_action_key}' triggered. Collecting data...")
    data_payload = {}
    spec_rendered = st.session_state.get('current_ui_spec')

    # Define which input types to collect data from
    INPUT_COMPONENT_TYPES = ["text_input", "selectbox", "text_area"] # Extend as needed

    if spec_rendered and isinstance(spec_rendered, list):
        for item in spec_rendered:
             if not isinstance(item, dict): continue
             comp_type = item.get("type")
             key = item.get("key")

             if key and comp_type in INPUT_COMPONENT_TYPES:
                 if key in st.session_state:
                     data_payload[key] = st.session_state[key]
                 else:
                     # Input might not have been rendered or state lost
                     data_payload[key] = None # Or log warning
                     st.warning(f"Could not find key '{key}' in session state during data collection.")

    st.write(f"DEBUG: Data collected: {data_payload}")
    # Logic for API call (Issue 3.6) will use data_payload
    # call_agent_simulator(triggered_action_key, data_payload, st.session_state.get("task_id"))
    pass
```

3. Run the app, go to a form view, enter text, click the button. Verify the debug message shows the collected data correctly.
