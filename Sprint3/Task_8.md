# Issue 3.8: Define & Document API Contract (OpenAPI V1.0)

## Description
Create and commit an openapi.yaml (or JSON) file using OpenAPI Specification v3.x. Define the GET /ui_spec endpoint (with optional task_id query parameter) and the POST /interact endpoint. Specify request bodies (including action_key, data, placeholder user_id, optional task_id) and response schemas (including status, view_config, message fields).

## Acceptance Criteria
- openapi.yaml file exists in the repository
- It defines the two endpoints, their parameters, and basic request/response structures matching the simulator's behavior and planned data flow

## Estimate
Medium

## Execution Steps
1. Create a file named openapi.yaml in the project root (or a docs folder)
2. Add the basic OpenAPI structure:
```yaml
openapi: 3.0.0
info:
  title: Agent UI Interaction API (MVP V1.0)
  version: 1.0.0
  description: API for Streamlit frontend to interact with the Agent Logic (Simulator for MVP).
servers:
  - url: http://localhost:5001 # Simulator URL for MVP testing
    description: Local Agent Simulator
paths:
  # Definition for GET /ui_spec
  /ui_spec:
    get:
      summary: Get initial UI specification
      parameters:
        - name: task_id
          in: query
          required: false
          schema:
            type: string
          description: Optional ID for a specific task context.
        - name: user_id # Added based on later steps, good to define early
          in: query # Or maybe header later? Define how initial load gets user ID
          required: true # Assuming required after login
          schema:
            type: string
          description: Identifier of the logged-in user.
      responses:
        '200':
          description: Successful response with UI view configuration.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApiResponse'
        # Add other potential responses like 403, 500 later

  # Definition for POST /interact
  /interact:
    post:
      summary: Send user interaction and get next UI spec
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InteractionRequest'
      responses:
        '200':
          description: Successful interaction, returns next UI view configuration or status.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApiResponse'
        # Add other potential responses like 400, 403, 500 later

components:
  schemas:
    InteractionRequest:
      type: object
      properties:
        action_key:
          type: string
          description: The unique key of the element that triggered the interaction.
        data:
          type: object
          description: Key-value pairs of data collected from input elements related to the action.
          additionalProperties: true
        task_id:
          type: string
          nullable: true
          description: The context task ID, if applicable.
        user_id:
          type: string
          description: Identifier of the logged-in user performing the action.
      required:
        - action_key
        - data
        - user_id

    ApiResponse:
      type: object
      properties:
        status:
          type: string
          enum: [success, error, access_denied]
          description: Outcome of the request.
        view_config:
          type: array # Assuming spec is a list of objects
          items:
             type: object # Define component structure more strictly later if needed
          nullable: true
          description: The UI specification to render next (only on success).
        message:
          type: string
          nullable: true
          description: Optional message, especially for error or access denied status.
      required:
        - status
```

3. Commit this initial openapi.yaml file to the repository
4. Use tools like Swagger Editor online to validate the syntax
