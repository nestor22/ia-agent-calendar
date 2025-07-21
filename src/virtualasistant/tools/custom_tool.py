from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
from googleapiclient.discovery import build


# Alcances necesarios para Google Calendar


def get_calendar_service_with_api_key():
    """Crea el servicio usando solo API key."""
    api_key = os.getenv('GOOGLE_CALENDAR_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_CALENDAR_API_KEY no está configurado")
    
    service = build('calendar', 'v3', developerKey=api_key)
    return service

class CalendarEventInput(BaseModel):
    """Input schema for the calendar on google."""
    events_data: str = Field(..., description="data from the events in JSON format")

class GoogleCalendarTool(BaseTool):
    name: str = "google_calendar_creator"
    description: str = (
        "Create events in the google calendar base on the report"
    )
    args_schema: Type[BaseModel] = CalendarEventInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        try:
               # Parsear los datos de eventos
            events = json.loads(events_data)
            
            service = get_calendar_service_with_api_key()
            
            created_events = []
            for event_data in events:
                event = {
                    'summary': event_data.get('title', 'Evento sin título'),
                    'start': {
                        'dateTime': event_data.get('start_time'),
                        'timeZone': 'America/Mexico_City',
                    },
                    'end': {
                        'dateTime': event_data.get('end_time'),
                        'timeZone': 'America/Mexico_City',
                    },
                    'description': event_data.get('description', ''),
                    'location': event_data.get('location', ''),
                }
                
                created_event = service.events().insert(
                    calendarId='Tasks', 
                    body=event
                ).execute()
                
                created_events.append(created_event['id'])
            return f"Se crearon {len(created_events)} eventos exitosamente" 
        except Exception as e:
            return f"Error al crear eventos: {str(e)}"
