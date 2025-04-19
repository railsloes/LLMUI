from flask import Flask, jsonify
import random

app = Flask(__name__)

# --- Define UI Specifications (Same as in app.py for now) ---
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

# Spec V3: Minimal spec with just text elements
SPEC_V3 = [
     {"type": "markdown", "text": "## Agent Interface V3\n\nThis is a minimal interface from the service."},
     {"type": "text_area", "label": "Note (Service)", "key": "v3_note"}
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

# --- All Specs --- 
ALL_SPECS = {
    "V1": SPEC_V1,
    "V2": SPEC_V2,
    "V3": SPEC_V3,
    "V4": SPEC_V4 # Added V4
}

@app.route('/get_spec', methods=['GET'])
def get_random_spec():
    """Returns a random UI specification."""
    random_version = random.choice(list(ALL_SPECS.keys()))
    print(f"Serving random spec: {random_version}")
    return jsonify(ALL_SPECS[random_version])

@app.route('/get_spec/<version>', methods=['GET'])
def get_specific_spec(version):
    """Returns a specific UI specification by version."""
    spec = ALL_SPECS.get(version.upper()) # Use upper() for case-insensitivity
    if spec:
        print(f"Serving spec: {version.upper()}")
        return jsonify(spec)
    else:
        print(f"Spec version not found: {version}")
        return jsonify({"error": f"Specification version '{version}' not found. Available: {list(ALL_SPECS.keys())}"}), 404

if __name__ == '__main__':
    # Note: Use 'flask run --port 5001' in production or via a WSGI server
    # For simple testing, you can run this script directly:
    # app.run(debug=True, port=5001)
    # Production WSGI example: gunicorn --bind 0.0.0.0:5001 remote_agent_simulation:app
    print("Starting Remote Agent Simulation. Use 'flask --app remote_agent_simulation run --port 5001' to run.")
