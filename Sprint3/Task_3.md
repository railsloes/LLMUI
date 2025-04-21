# Issue 3.3: Implement Interaction Detection (Key Iteration)

## Description
In app.py, after the render_ui call, implement the post-render loop to iterate through the interactive elements (buttons initially) defined in the currently rendered UI spec (st.session_state.current_ui_spec). Use element keys to check st.session_state and identify which button was clicked (triggered_action_key).

## Acceptance Criteria
- When a button rendered via render_ui is clicked, the script correctly identifies the key of the clicked button after the rerun
- Only one action key is identified per cycle

## Estimate
Medium

## Dependencies
- Completed Step 1 (render_ui basics)

## Execution Steps
1. In app.py, locate the main part of the script after the render_ui(spec_to_render) call
2. Add the interaction detection logic:
```python
# --- Interaction Handling ---
triggered_action_key = None
spec_rendered = st.session_state.get('current_ui_spec') # Get the spec that was just rendered

if spec_rendered and isinstance(spec_rendered, list):
    for item in spec_rendered:
        if not isinstance(item, dict): continue

        comp_type = item.get("type")
        key = item.get("key")

        if not key: continue # Skip elements without keys

        # Check for button clicks
        if comp_type == "button":
            if st.session_state.get(key): # Check if button state is True
                triggered_action_key = key
                st.write(f"DEBUG: Detected button click for key: {key}") # Debug
                # State reset will be added in Issue 3.4
                break # Process only the first detected action

        # Add elif checks for other interactive types later if needed

# --- Action Processing (Placeholder) ---
if triggered_action_key:
    st.write(f"DEBUG: Action '{triggered_action_key}' triggered. Proceeding...")
    # Logic for data collection (Issue 3.5) and API call (Issue 3.6) will go here
    pass
```

3. Run the app, navigate to a view with a button, click the button, and verify the debug message appears showing the correct key.
