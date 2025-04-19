Here is a detailed list of tasks, including execution steps, to build the PoC:Task 1: Project SetupDescription: Create the project directory, set up a Python virtual environment (venv), and install Streamlit. Create the main app.py file and a requirements.txt file.Acceptance Criteria: A directory exists with venv, requirements.txt listing streamlit, and a minimal runnable app.py. .gitignore is present.Estimate: SExecution Steps:Open your terminal or command prompt.Create the project directory: mkdir poc_streamlit_coreNavigate into the directory: cd poc_streamlit_coreCreate a Python virtual environment: python -m venv venvActivate the virtual environment:Linux/macOS: source venv/bin/activateWindows (Command Prompt): venv\Scripts\activate.batWindows (PowerShell): venv\Scripts\Activate.ps1Install Streamlit: pip install streamlitGenerate the requirements file: pip freeze > requirements.txtCreate the main application file: touch app.py (Linux/macOS) or create a new file named app.py using your editor.Add initial content to app.py:import streamlit as st

st.set_page_config(layout="wide") # Optional: Use wider layout
st.title("PoC: Streamlit Dynamic UI Core")
st.markdown("Initial application structure.")
Create a .gitignore file: touch .gitignore (Linux/macOS) or create the file.Add lines to .gitignore to ignore the virtual environment and Streamlit secrets directory:venv/
.streamlit/
__pycache__/
*.pyc
Run the app to verify: streamlit run app.py. You should see the title and markdown text in your browser.Task 2: Define Predefined UI SpecsDescription: Within app.py, define three Python dictionary variables: TEXT_SPEC, FORM_SPEC, CHAT_SPEC.TEXT_SPEC: Should contain at least one {"component": "markdown", "text": "This is the text view."}.FORM_SPEC: Should contain at least two {"component": "text_input", "label": "...", "key": "unique_form_key_1"} elements and potentially a placeholder {"component": "button", "label": "Submit (Placeholder)", "key": "form_submit_btn"}. Ensure input keys are unique.CHAT_SPEC: Should contain at least two {"component": "chat_message", "role": "...", "text": "..."} elements (e.g., one user, one assistant).Acceptance Criteria: Three variables exist in app.py containing valid dictionary structures representing the UI specs for the three views, including keys for form inputs.Estimate: SExecution Steps:Open app.py in your code editor.Below the initial imports and title, define the Python dictionaries:import streamlit as st

st.set_page_config(layout="wide")
st.title("PoC: Streamlit Dynamic UI Core")

# --- Define UI Specifications ---

TEXT_SPEC = [
    {"component": "markdown", "text": "## Text View\n\nThis view displays simple static text content."},
    {"component": "markdown", "text": "Rendered from `TEXT_SPEC`."}
]

FORM_SPEC = [
    {"component": "markdown", "text": "## Form View\n\nEnter details below. Values should persist when switching views."},
    {"component": "text_input", "label": "First Name", "key": "form_first_name"},
    {"component": "text_input", "label": "Last Name", "key": "form_last_name", "type": "default"}, # Explicitly default type
    {"component": "button", "label": "Submit (Placeholder Action)", "key": "form_submit_button"}
]

CHAT_SPEC = [
    {"component": "markdown", "text": "## Chat View\n\nDisplays a simple chat history."},
    {"component": "chat_message", "role": "user", "text": "Hello Agent!"},
    {"component": "chat_message", "role": "assistant", "text": "Hello User! How can I help?"}
]

# (Rest of the app logic will go here)
Save the app.py file.Task 3: Implement Basic render_ui FunctionDescription: Create the render_ui(spec) function. It should accept a spec dictionary (like those defined in Task 2). Implement logic to iterate through the spec items and render st.markdown, st.text_input, st.button, and st.chat_message based on the "component" type. Pass relevant attributes (text, label, key, role) to the Streamlit functions. Include basic handling for unknown component types (e.g., st.warning).Acceptance Criteria: The render_ui function exists and can successfully render the components defined in the MVP specs when passed the corresponding dictionary.Estimate: MExecution Steps:In app.py, below the spec definitions, define the render_ui function:# --- UI Rendering Function ---

def render_ui(spec):
    """Renders Streamlit UI elements based on a list-of-dicts specification."""
    if not isinstance(spec, list):
        st.error("Invalid UI specification format: Expected a list.")
        return

    for item in spec:
        if not isinstance(item, dict):
            st.warning("Skipping invalid item in UI spec (not a dict).")
            continue

        comp_type = item.get("component")
        key = item.get("key") # Pass key to interactive elements

        try:
            if comp_type == "markdown":
                st.markdown(item.get("text", ""), unsafe_allow_html=False)
            elif comp_type == "text_input":
                # Get optional 'type' (default is 'default')
                input_type = item.get("type", "default")
                st.text_input(
                    label=item.get("label", ""),
                    key=key,
                    help=item.get("help"),
                    type=input_type # Pass type (e.g., 'default', 'password')
                )
            elif comp_type == "button":
                st.button(label=item.get("label", "Button"), key=key)
            elif comp_type == "chat_message":
                role = item.get("role", "assistant")
                avatar = item.get("avatar")
                with st.chat_message(name=role, avatar=avatar):
                    st.markdown(item.get("text", ""))
            # Add elif for other components like title, selectbox, metric, columns later if needed
            elif comp_type: # Only warn if component type was specified but not matched
                st.warning(f"Unsupported component type: '{comp_type}' for key '{key}'.")

        except Exception as e:
            st.error(f"Error rendering component (key={key}, type={comp_type}): {e}")

# (Rest of the app logic will go here)
Save the app.py file.Task 4: Implement State Management & Initial ViewDescription: Use st.session_state to manage the active view. Initialize st.session_state['current_view'] = 'text' if it doesn't exist. Based on the value of st.session_state['current_view'], select the correct spec dictionary (TEXT_SPEC, FORM_SPEC, or CHAT_SPEC) and pass it to the render_ui function.Acceptance Criteria: The app starts and correctly renders the TEXT_SPEC UI by default using the render_ui function and st.session_state.Estimate: SDepends on: Task 2, Task 3Execution Steps:In app.py, below the render_ui function definition, add the state management and rendering logic:# --- State Management and Main Rendering Logic ---

# Initialize session state for the current view if it doesn't exist
if 'current_view' not in st.session_state:
    st.session_state['current_view'] = 'text' # Default view

# Determine which spec to render based on the current state
if st.session_state['current_view'] == 'text':
    spec_to_render = TEXT_SPEC
elif st.session_state['current_view'] == 'form':
    spec_to_render = FORM_SPEC
elif st.session_state['current_view'] == 'chat':
    spec_to_render = CHAT_SPEC
else:
    # Fallback or error case
    st.error(f"Unknown view state: {st.session_state['current_view']}")
    spec_to_render = [{"component": "markdown", "text": "**Error:** Invalid view state."}]

# Render the selected UI specification
st.header(f"Current View: {st.session_state['current_view'].capitalize()}")
st.divider()
render_ui(spec_to_render)

# Add view switching buttons (Task 5 will place them properly)
st.divider()
st.subheader("View Navigation (Placeholder Location)")
# (Button logic will go here in Task 5)

# Optional: Display session state for debugging
st.divider()
with st.expander("Show Session State (Debug)"):
     st.json(st.session_state.to_dict())
Save app.py.Run streamlit run app.py. Verify the app loads, shows "Current View: Text", and renders the markdown from TEXT_SPEC. Check the debug expander.Task 5: Implement View Switching Buttons & LogicDescription: Add three persistent st.button widgets (e.g., in the sidebar or using st.columns at the top/bottom): "Show Text", "Show Form", "Show Chat". Implement the logic so that clicking each button updates st.session_state['current_view'] to 'text', 'form', or 'chat' respectively.Acceptance Criteria: The three buttons are always visible. Clicking a button updates the main view to display the UI corresponding to that button's spec via the render_ui function on the next rerun.Estimate: MDepends on: Task 4Execution Steps:In app.py, modify the placeholder section for navigation buttons. Using the sidebar is often cleanest:# --- View Navigation Buttons (in Sidebar) ---
st.sidebar.header("Change View")

if st.sidebar.button("Show Text", key="nav_text_btn"):
    st.session_state['current_view'] = 'text'
    # Optional: Immediately rerun to reflect change if needed,
    # though Streamlit usually handles rerun on button click.
    # st.rerun()

if st.sidebar.button("Show Form", key="nav_form_btn"):
    st.session_state['current_view'] = 'form'
    # st.rerun()

if st.sidebar.button("Show Chat", key="nav_chat_btn"):
    st.session_state['current_view'] = 'chat'
    # st.rerun()

# Remove the placeholder section from the main area if you added it before.
Save app.py.Run streamlit run app.py.Verify the three buttons appear in the sidebar.Click each button and confirm that the main view area updates to show the corresponding content ("Text View", "Form View", "Chat View") and the "Current View" header changes. Check the session state debug area to see current_view update.Task 6: Test Form State PersistenceDescription: Run the application. Navigate to the "Form View". Enter distinct values into the text input fields. Navigate away to the "Text View" or "Chat View" using the buttons. Navigate back to the "Form View". Verify that the values previously entered into the text input fields are still present.Acceptance Criteria: Input values within the Form View persist correctly when switching between views, demonstrating st.session_state working with widget keys.Estimate: SDepends on: Task 5Execution Steps:Ensure the app is running (streamlit run app.py).Click the "Show Form" button in the sidebar.In the "First Name" input field, type "TestFirstName".In the "Last Name" input field, type "TestLastName".Click the "Show Text" button in the sidebar. Observe the text view.Click the "Show Form" button again.Verify: The "First Name" field should still contain "TestFirstName", and the "Last Name" field should still contain "TestLastName". This works because the render_ui function consistently assigns the same key ("form_first_name", "form_last_name") to these inputs, and Streamlit automatically stores widget values in st.session_state using their keys.Task 7: Prepare for DeploymentDescription: Ensure the requirements.txt file accurately lists only streamlit (and any other direct, necessary dependencies, though none are expected for this PoC). Add a simple README.md explaining how to run the PoC locally. Test the application thoroughly one last time.Acceptance Criteria: requirements.txt is correct. README.md exists with basic instructions. App is ready for potential deployment to Streamlit Community Cloud.Estimate: S