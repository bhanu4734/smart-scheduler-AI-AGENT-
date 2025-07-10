# 📅 AI Calendar Scheduler with OpenAI & Google Calendar

This project is a smart calendar scheduler built using **Flask**, **OpenAI GPT-4**, and **Google Calendar API**. It allows users to input natural language text like:

> “Schedule a meeting with John next Friday at 3 PM about the sales report”

The app will:
- Extract event details using GPT-4
- Parse the date and time
- Create a new event in your Google Calendar
- Set up a custom reminder

---

## 🚀 Features

- 🔍 Extracts structured event details using OpenAI GPT-4
- 📅 Creates Google Calendar events with custom duration & reminders
- 🧠 Natural language input for intuitive scheduling
- 🕒 Lists upcoming 10 events from your calendar
- 🌐 Simple web interface (HTML + Flask)

---

## 📦 Requirements

- Python 3.7+
- Google Calendar API credentials (`credentials.json`)
- OpenAI API Key

---

## 🔧 Installation

1. **Clone the repository**

   git clone https://github.com/yourusername/ai-calendar-scheduler.git
   cd ai-calendar-scheduler

2. **Install dependencies**

        pip install -r requirements.txt

3. **Add credentials**

    Download your credentials.json from Google Cloud Console

    Place it in the root directory

4. **Add your OpenAI API key**

    In app.py, replace: openai.api_key = 'your-api-key-here'

**▶️ Running the App**

             python app.py

             Visit: http://127.0.0.1:5000

            **Use tools like Postman or cURL to POST data to /schedule**

**📤 API Endpoints**

    **POST /schedule** 

                    Body (JSON):
                           
                                {
                                    "text": "Schedule meeting with Sarah tomorrow at 2pm about product design",
                                    "duration": 45,
                                    "reminder": 15
                                }

                    Response:

                                {
                                    "message": "✅ Event created",
                                    "event": { ...event metadata... }
                                }

**GET /events**

Returns the next 10 upcoming Google Calendar events in JSON format.          

**🧠 How It Works**

1.User inputs natural language text.

2.GPT-4 extracts:

    person

    date_time

    description

    dateparser converts the extracted time string into a Python datetime.

3.Google Calendar API schedules the event with reminders.

4.Google Calendar API schedules the event with reminders.

**🔐 Authentication & Permissions**

1.Requires Google account authorization via OAuth2.

2.Stores the access token locally after first use.

**🛡️ Security Notes**

1.DO NOT share your OpenAI API key publicly.

2.Keep your credentials.json file safe and out of version control (.gitignore it).