1. Purpose

The primary goal of this PoC is to validate and demonstrate the core Streamlit mechanisms required for the larger project:

Dynamically rendering a user interface based on a predefined data structure (JSON/Dictionary specification).

Using Streamlit's session_state to manage the current UI view.

Implementing a basic interaction loop where user actions (button clicks) trigger updates to the session_state, leading to a re-render of a different predefined UI view.

Verifying that input elements within a dynamically rendered view retain their state across view switches (leveraging st.session_state and widget keys).

2. Scope & Simplifications

Frontend Only: This PoC involves only a Streamlit application (app.py). No backend Agent Logic server or API calls will be implemented.

No Authentication: User login/authentication is explicitly excluded.

Predefined UI Specs: Three distinct UI view specifications (Text View, Form View, Chat View) will be hardcoded as Python dictionaries within the app.py script.

Simple Interaction: Three persistent buttons will allow the user to switch between the three predefined views.

Basic Components: The UI specs will use a minimal set of Streamlit components (e.g., st.markdown, st.text_input, st.button, st.chat_message).

State Management: st.session_state will be used solely to track which of the three predefined views is currently active.

Deployment Target: The final PoC code should be structured as a standard Streamlit application deployable to Streamlit Community Cloud.

3. Functionality

The application starts and displays the "Text View" by default.

Three buttons ("Show Text", "Show Form", "Show Chat") are always visible (e.g., in the sidebar or a dedicated top/bottom section).

Clicking the "Show Form" button updates the main application area to display the UI defined by the "Form View" spec.

Clicking the "Show Chat" button updates the main area to display the UI defined by the "Chat View" spec.

Clicking the "Show Text" button updates the main area to display the UI defined by the "Text View" spec.

When the "Form View" is displayed, the user can enter text into its input fields. If the user navigates away to the "Text" or "Chat" view and then back to the "Form" view, the previously entered text should still be present in the input fields.

4. Technical Approach

Core Script: A single app.py file.

UI Specs: Define three Python dictionaries (TEXT_SPEC, FORM_SPEC, CHAT_SPEC) directly in the script. FORM_SPEC must include key attributes for its input elements.

State: Use st.session_state['current_view'] initialized to 'text'.

Rendering Function: A simple render_ui(spec) function that takes one of the spec dictionaries and uses if/elif blocks to call the corresponding st.* functions based on the "component" type defined in the spec items.

Interaction Buttons: Three st.button widgets. Clicking a button will update st.session_state['current_view'] to the corresponding view identifier ('text', 'form', or 'chat'). This update will trigger a Streamlit rerun, causing the render_ui function to be called with the new spec based on the updated state.

Dependencies: Only streamlit is required (requirements.txt).