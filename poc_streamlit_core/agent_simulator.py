from flask import Flask, jsonify, request
import random
import json
import time

app = Flask(__name__)

# --- Define UI Specifications ---
# You can load these from files or generate them dynamically

SPEC_V1 = [
    {"type": "markdown", "text": "# Agent Interface V1\n\nFetched from **Local Service**."},
    {"type": "divider"},
    {"type": "data_entry_form", "key": "task_form", "elements": [
        {"type": "text_input", "label": "Task Title (Service)", "key": "task_title"},
        {"type": "selectbox", "label": "Priority", "key": "task_priority", "options": ["Low", "Medium", "High"]}
    ]}
]

SPEC_V2 = [
    {"type": "markdown", "text": "# Agent Interface V2\n\nFetched from **Local Service**."},
    {"type": "divider"},
    {"type": "data_entry_form", "key": "quick_task_form", "elements": [
        {"type": "text_input", "label": "Task Name (Service)", "key": "quick_task_name"},
        {"type": "selectbox", "label": "Priority", "key": "quick_task_priority", "options": ["Low", "High"]}
    ]}
]

# Spec V3: Minimal spec with text elements and test buttons
SPEC_V3 = [
     {"type": "markdown", "text": "## Agent Interface V3 (DEBUG VERSION)\n\nThis is a minimal interface from the service with test buttons."},
     {"type": "text_area", "label": "Note (Service)", "key": "v3_note"},
     {"type": "divider"},
     {"type": "markdown", "text": "### Test Buttons for Interaction Detection"},
     {"type": "button", "label": "Click Me for Testing", "key": "v3_test_button"},
     {"type": "button", "label": "Second Test Button", "key": "v3_test_button2"},
     {"type": "markdown", "text": "### Debug Info"},
     {"type": "markdown", "text": "If you can see this text, the spec is being rendered correctly."}
]

# Spec V4: Demonstrates the use of st.tabs
SPEC_V4 = [
    {"type": "markdown", "text": "# Agent Interface V4 (with Tabs)"}, 
    {
        "type": "tabs",
        "names": ["Dashboard", "Task Entry", "Chat"], # Tab titles
        "children": [
            # Content for Tab 1: Dashboard (using columns)
            [
                {"type": "markdown", "text": "## Dashboard Overview"},
                {
                    "type": "columns",
                    "spec": [1, 1], 
                    "children": [
                        [
                            {"type": "markdown", "text": "### User Info"},
                            {"type": "markdown", "text": "**Name**: Jane Smith\n**Role**: Analyst"}
                        ],
                        [
                            {"type": "markdown", "text": "### Project Stats"},
                            {"type": "markdown", "text": "**Active**: 3\n**Completed**: 15"}
                        ]
                    ]
                },
                 {"type": "divider"},
                 {"type": "markdown", "text": "Some stats or charts could go here."}
            ],
            # Content for Tab 2: Task Entry (using a form)
            [
                {"type": "markdown", "text": "## Enter New Task"},
                {
                    "type": "data_entry_form",
                    "key": "v4_task_form",
                    "elements": [
                        {"type": "text_input", "label": "Task Name", "key": "v4_task_name"},
                        {"type": "selectbox", "label": "Assignee", "key": "v4_task_assignee", "options": ["Jane", "Peter", "Linda"]},
                        {"type": "text_area", "label": "Details", "key": "v4_task_details"}
                    ]
                }
            ],
            # Content for Tab 3: Chat (using chat interface)
            [
                {"type": "markdown", "text": "## Agent Chat Interface"},
                {
                    "type": "chat_interface",
                    "key": "v4_agent_chat",
                    "history": [
                         {"role": "assistant", "content": "Welcome to the V4 interface chat!"}
                    ]
                }
            ]
        ]
    }
]

# Spec V5: Demonstrates conditional UI elements
SPEC_V5 = [
    {"type": "markdown", "text": "# Agent Interface V5 (Conditional UI)\n\nThis interface demonstrates conditional UI elements and partial updates."},
    {"type": "divider"},
    
    # Preference selection that affects what's shown below
    {"type": "markdown", "text": "### Basic Information", "key": "v5_basic_section"},
    {"type": "text_input", "label": "Title", "key": "v5_title"},
    {"type": "text_area", "label": "Description", "key": "v5_description"},
    
    {"type": "divider"},
    
    # View mode selection
    {"type": "markdown", "text": "### Display Preferences"},
    {"type": "selectbox", "label": "View Mode", "key": "v5_view_mode", 
     "options": ["Simple", "Advanced", "Developer"]},
    
    # Dropdown to toggle optional fields
    {"type": "selectbox", "label": "Show Optional Fields", "key": "v5_show_optional", "options": ["No", "Yes"]},
    
    {"type": "divider"},
    
    # Button to refresh the view
    {"type": "button", "label": "Refresh View", "key": "v5_refresh_button"},
    
    # This element only shows if show_optional is checked
    {"type": "text_input", "label": "Tags (Optional)", "key": "v5_tags"},
    
    # This element only shows in Developer mode
    {"type": "text_area", "label": "Technical Notes", "key": "v5_tech_notes"},
    
    {"type": "divider"},
    
    # Button to submit the form
    {"type": "button", "label": "Submit", "key": "v5_submit_button"},
    
    # Status area that will be updated by partial updates
    {"type": "markdown", "text": "Status: Ready", "key": "v5_status"}
]

# Spec V6: Email-Based Access Control Demo
SPEC_V6 = [
    {"type": "markdown", "text": "# Project Management Dashboard\n\nWelcome to the project management system."},
    {"type": "divider"},
    
    # User info section - will show the current user's email and access level
    {"type": "markdown", "text": "### User Information", "key": "v6_user_section"},
    {"type": "markdown", "text": "Loading user information...", "key": "v6_user_info"},
    
    {"type": "divider"},
    
    # Project overview - visible to all users
    {"type": "markdown", "text": "### Project Overview"},
    {"type": "markdown", "text": "**Active Projects:** 5\n**Completed Projects:** 12\n**Team Members:** 8"},
    
    # Project creation form - only visible to admin users
    {"type": "markdown", "text": "### Create New Project (Admin Only)", "key": "v6_admin_section"},
    {"type": "text_input", "label": "Project Name", "key": "v6_project_name"},
    {"type": "text_area", "label": "Project Description", "key": "v6_project_description"},
    {"type": "selectbox", "label": "Priority", "key": "v6_project_priority", 
     "options": ["Low", "Medium", "High", "Critical"]},
    {"type": "button", "label": "Create Project", "key": "v6_create_project"},
    
    {"type": "divider"},
    
    # System configuration - only visible to admin users
    {"type": "markdown", "text": "### System Configuration (Admin Only)", "key": "v6_config_section"},
    {"type": "selectbox", "label": "Enable Advanced Features", "key": "v6_enable_advanced", "options": ["No", "Yes"]},
    {"type": "selectbox", "label": "Allow Guest Access", "key": "v6_allow_guests", "options": ["No", "Yes"]},
    {"type": "button", "label": "Save Configuration", "key": "v6_save_config"},
    
    {"type": "divider"},
    
    # Task list - different views for admin vs regular users
    {"type": "markdown", "text": "### My Tasks", "key": "v6_tasks_section"},
    {"type": "markdown", "text": "Loading tasks...", "key": "v6_tasks_list"},
    
    # Action buttons - different capabilities for admin vs regular users
    {"type": "button", "label": "Refresh Tasks", "key": "v6_refresh_tasks"},
    {"type": "button", "label": "Generate Report (Admin Only)", "key": "v6_generate_report"}
]

# --- All Specs --- 
ALL_SPECS = {
    "V1": SPEC_V1,
    "V2": SPEC_V2,
    "V3": SPEC_V3,
    "V4": SPEC_V4,
    "V5": SPEC_V5,
    "V6": SPEC_V6  # Added V6 with email-based access control
}

# --- Response Spec for Interactions ---
# This is the spec that will be returned when an interaction is received
CHAT_SPEC = [
    {"type": "markdown", "text": "# Chat View After Interaction\n\nThis view is shown after an interaction was processed."},
    {"type": "chat_interface", "key": "agent_chat", "history": [
        {"role": "assistant", "content": "I've received your interaction! Here's what you sent:"}
    ]}
]

# --- API Endpoints ---

@app.route('/get_spec', methods=['GET'])
def get_random_spec():
    """Returns a random UI specification."""
    random_version = random.choice(list(ALL_SPECS.keys()))
    print(f"Serving random spec: {random_version}")
    return jsonify(ALL_SPECS[random_version])

@app.route('/get_spec/<version>', methods=['GET'])
def get_specific_spec(version):
    """Returns a specific UI specification by version.
    Also prints the task_id if provided in query parameters.
    
    Enhanced in Sprint 5 to support email-based access control for SPEC_V6.
    """
    task_id = request.args.get('task_id')  # Get task_id from query params
    user_id = request.args.get('user_id')  # Get user_id (email) from query params
    
    # Get the requested spec
    spec = ALL_SPECS.get(version.upper())  # Use upper() for case-insensitivity
    
    if spec:
        print(f"Serving spec: {version.upper()}. Received task_id: {task_id}, user_id: {user_id}")  # Print task_id and user_id
        
        # SPRINT 5: Customize SPEC_V6 based on user's email
        if version.upper() == "V6" and user_id:
            # Create a copy of the spec to customize
            custom_spec = spec.copy()
            
            # Determine access level based on email
            is_admin = user_id == "feloes@gmail.com"
            access_level = "Admin" if is_admin else "Regular User"
            
            # Update the user info section
            for item in custom_spec:
                if item.get("key") == "v6_user_info":
                    item["text"] = f"**Email:** {user_id}\n**Access Level:** {access_level}"
                
                # For regular users, remove admin-only sections or disable them
                if not is_admin:
                    # Hide admin-only sections by setting their text to indicate no access
                    if item.get("key") == "v6_admin_section":
                        item["text"] = "### Create New Project (Restricted Access)"
                    elif item.get("key") == "v6_config_section":
                        item["text"] = "### System Configuration (Restricted Access)"
            
            # Return the customized spec
            return jsonify(custom_spec)
        
        # For other specs, return as is
        return jsonify(spec)
    else:
        print(f"Spec version not found: {version}. Received task_id: {task_id}")  # Also print here
        return jsonify({"error": f"Specification version '{version}' not found. Available: {list(ALL_SPECS.keys())}"}), 404

@app.route('/interact', methods=['POST'])
def interact():
    """Handles user interactions with the UI.
    Receives action_key, data_payload, and task_id from the Streamlit app.
    Returns a new UI spec to display.
    
    Enhanced in Sprint 5 to support email-based access control.
    """
    try:
        # Get the JSON payload from the request
        payload = request.get_json()
        
        # Log the received payload
        print("SIMULATOR: Received POST /interact with payload:")
        print(json.dumps(payload, indent=2))
        
        # Extract the data from the payload
        action_key = payload.get("action_key")
        data = payload.get("data", {})
        task_id = payload.get("task_id")
        user_id = payload.get("user_id", "anonymous")
        
        # Basic validation
        if not action_key:
            return jsonify({"status": "error", "message": "Missing action_key"}), 400
        
        # SPRINT 5: Handle V6 actions with email-based access control
        if action_key.startswith("v6_"):
            # Create a copy of SPEC_V6 to customize based on user's email
            custom_spec = SPEC_V6.copy()
            
            # Determine access level based on email
            is_admin = user_id == "feloes@gmail.com"
            access_level = "Admin" if is_admin else "Regular User"
            
            # Update the user info section
            for item in custom_spec:
                if item.get("key") == "v6_user_info":
                    item["text"] = f"**Email:** {user_id}\n**Access Level:** {access_level}"
                
                # For regular users, remove admin-only sections
                if not is_admin:
                    # Hide admin-only sections by setting their text to indicate no access
                    if item.get("key") == "v6_admin_section":
                        item["text"] = "### Create New Project (Restricted Access)"
                    elif item.get("key") == "v6_config_section":
                        item["text"] = "### System Configuration (Restricted Access)"
            
            # Process specific actions
            if action_key == "v6_refresh_tasks":
                # Update the tasks list based on user's access level
                for item in custom_spec:
                    if item.get("key") == "v6_tasks_list":
                        if is_admin:
                            item["text"] = "**Task 1:** Review project proposals (High)\n**Task 2:** Approve budget requests (Medium)\n**Task 3:** Configure system settings (Low)"
                        else:
                            item["text"] = "**Task 1:** Submit weekly report (Medium)\n**Task 2:** Update project documentation (Low)"
            
            elif action_key == "v6_generate_report" and is_admin:
                # Only admins can generate reports
                for item in custom_spec:
                    if item.get("key") == "v6_tasks_section":
                        item["text"] = "### My Tasks (Report Generated)"
            
            # Return the customized spec
            return jsonify({
                "status": "success",
                "view_config": custom_spec
            })
        
        # Default behavior for other actions: return the chat spec
        chat_spec_with_data = CHAT_SPEC.copy()
        if isinstance(chat_spec_with_data, list) and len(chat_spec_with_data) > 1:
            # Find the chat interface component
            for item in chat_spec_with_data:
                if item.get("type") == "chat_interface" and "history" in item:
                    # Add a message showing the received data
                    item["history"].append({
                        "role": "assistant", 
                        "content": f"Action: {action_key}\nData: {json.dumps(data, indent=2)}\nTask ID: {task_id}\nUser ID: {user_id}"
                    })
                    break
        
        # Return success response with the chat spec
        response_data = {"status": "success", "view_config": chat_spec_with_data}
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in /interact endpoint: {str(e)}")
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    # Note: Use 'flask run --port 5001' in production or via a WSGI server
    # For simple testing, you can run this script directly:
    # app.run(debug=True, port=5001)
    # Production WSGI example: gunicorn --bind 0.0.0.0:5001 agent_simulator:app
    print("Starting Agent Simulator. Use 'flask --app agent_simulator run --port 5001' to run.")
