from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, os

SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None

flow = InstalledAppFlow.from_client_secrets_file('oauth_credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

with open('token_drive.pkl', 'wb') as token:
    pickle.dump(creds, token)

print("✅ Token generado correctamente")