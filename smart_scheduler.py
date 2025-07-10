from flask import Flask, request, jsonify, render_template
import openai
import dateparser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
import pytz
import json

app = Flask(__name__)
openai.api_key = 'OPEN_API_KEY'  # Replace with your actual key

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES).run_local_server(port=0)
calendar_service = build('calendar', 'v3', credentials=creds)

def extract_time_date(text):
    return dateparser.parse(text)

def get_event_details(prompt):
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{
            "role": "user",
            "content": f"Extract event details from: '{prompt}'. Format as JSON with keys: person, date_time, description."
        }]
    )
    return response.choices[0].message['content']

def create_event(summary, start_time, duration, reminder_minutes):
    end_time = start_time + timedelta(minutes=duration)
    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'reminders': {
            'useDefault': False,
            'overrides': [{'method': 'popup', 'minutes': reminder_minutes}]
        }
    }
    event_result = calendar_service.events().insert(calendarId='primary', body=event).execute()
    return event_result

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.json
    user_input = data.get("text")
    duration = int(data.get("duration", 60))
    reminder = int(data.get("reminder", 10))

    try:
        llm_response = get_event_details(user_input)
        parsed = json.loads(llm_response)
        event_time = extract_time_date(parsed['date_time'])

        if not event_time:
            return jsonify({"error": "Couldn't parse time."})

        event = create_event(parsed['description'], event_time, duration, reminder)
        return jsonify({"message": "✅ Event created", "event": event})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/events')
def list_events():
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = calendar_service.events().list(
        calendarId='primary', timeMin=now, maxResults=10,
        singleEvents=True, orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)
