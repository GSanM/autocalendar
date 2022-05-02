import datetime
import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from gcalendar.cal_setup import get_calendar_service

app = FastAPI()

class Event(BaseModel):
    summary: str
    description: Optional[str] = None
    start: dict
    end: dict

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/calendar")
async def get_calendar():
    service = get_calendar_service()
    # Call the Calendar API
    print('Getting list of calendars')
    calendars_result = service.calendarList().list().execute()

    calendars = calendars_result.get('items', [])

    if not calendars:
        return {"message": "No calendars found."}
    
    return calendars

@app.get("/calendar/{id}")
async def get_calendar(id):
    service = get_calendar_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(
        calendarId=id, timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return {"message": "No upcoming events found."}
    return events

@app.post("/calendar/{id}")
async def post_event(id, event: Event):
    service = get_calendar_service()

    event_result = service.events().insert(calendarId=id, body=event.dict()).execute()

    return event_result