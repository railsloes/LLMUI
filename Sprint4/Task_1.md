# Issue 4.1: Configure Google OIDC App Registration

## Description
Ensure Google Cloud Platform OAuth 2.0 Web Application client is correctly configured (consent screen, credentials, Redirect URIs). Securely document Client ID & Secret.

## Acceptance Criteria
- Credentials obtained/verified
- Redirect URIs (http://localhost:8501 and deployed URL) registered

## Estimate
Medium (If not done already) / Small (If just verifying)

## Execution Steps
1. Navigate to Google Cloud Console
2. Select or create a project
3. Go to "APIs & Services" -> "Credentials"
4. Click "+ CREATE CREDENTIALS" -> "OAuth client ID"
5. Select "Web application"
6. Give it a name (e.g., "Streamlit Agent UI Dev")
7. Under "Authorized redirect URIs", click "+ ADD URI" and add http://localhost:8501 (for local testing). Add your deployed app's base URL later if needed.
8. Click "Create"
9. Copy the "Client ID" and "Client Secret". Store them securely (e.g., password manager) - do not commit them.
10. Go to "APIs & Services" -> "OAuth consent screen"
11. Configure it (User Type: External/Internal, App name, User support email, Scopes - add openid, email, profile)
12. Ensure it's published or add test users if in testing mode
