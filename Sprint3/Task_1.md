# Issue 3.1: Handle task_id Parameter in Streamlit

## Description
Modify app.py to read the task_id query parameter from the URL upon page load using st.query_params. Store or pass this task_id for the initial API call to the simulator.

## Acceptance Criteria
- task_id from the URL (e.g., /?task_id=abc) is successfully read within the Streamlit script
- The initial GET /ui_spec call includes the task_id if present

## Estimate
Small

## Dependencies
- Completed Step 1 (Basic App Structure)

## Execution Steps
1. In app.py, add code to get query parameters:
```python
import streamlit as st

# Get query parameters
query_params = st.query_params

# Get task_id if it exists, default to None
task_id = query_params.get("task_id", [None])[0] # .get returns list

# Store it in session state if needed later, or just pass directly
if 'task_id' not in st.session_state:
   st.session_state.task_id = task_id
elif task_id: # Update if URL changes with a new task_id perhaps
   st.session_state.task_id = task_id

st.write(f"DEBUG: Detected Task ID: {st.session_state.task_id}") # Temporary debug
```

2. Modify the function making the initial GET /ui_spec call to include task_id as a query parameter if it's not None:
```python
# Example modification to an API call function
params = {}
current_task_id = st.session_state.get("task_id")
if current_task_id:
    params["task_id"] = current_task_id
# response = requests.get(simulator_url + "/ui_spec", params=params)
```

3. Test by running streamlit run app.py and then accessing http://localhost:8501/?task_id=my_test_task in your browser. Verify the debug message shows my_test_task.
