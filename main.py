import json
import base64
from flask import Flask, jsonify
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

app = Flask(__name__)

KEY_BASE64 = """ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3Rf...SUA_CHAVE_BASE64..."""

SHEET_ID = "SUA_PLANILHA_ID"
SHEET_RANGE = "HH_OUT!B:C"

def get_sheet_data():
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    key_dict = json.loads(base64.b64decode(KEY_BASE64))
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scopes=scopes)

    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=SHEET_ID, range=SHEET_RANGE).execute()
    values = result.get('values', [])
    return values

@app.route("/dados", methods=["GET"])
def dados():
    try:
        data = get_sheet_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
