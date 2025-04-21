# Issue 4.2: Configure Microsoft OIDC App Registration

## Description
Ensure Azure AD / Microsoft Entra ID App Registration is correctly configured (Web platform, account types, credentials, Redirect URIs). Securely document Client ID & Secret.

## Acceptance Criteria
- Credentials obtained/verified
- Redirect URIs registered

## Estimate
Medium (If not done already) / Small (If just verifying)

## Execution Steps
1. Navigate to the Microsoft Entra admin center or Azure portal
2. Go to "Microsoft Entra ID" -> "App registrations"
3. Click "+ New registration"
4. Give it a name (e.g., "Streamlit Agent UI Dev")
5. Select desired "Supported account types" (e.g., "Accounts in any organizational directory (Any Microsoft Entra ID tenant - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)")
6. Under "Redirect URI", select "Web" and enter http://localhost:8501. Add deployed URL later.
7. Click "Register"
8. Copy the "Application (client) ID". Store securely.
9. Go to "Certificates & secrets" -> "Client secrets" -> "+ New client secret"
10. Add a description, choose expiry, click "Add"
11. Immediately copy the secret Value. Store securely - it won't be shown again.
