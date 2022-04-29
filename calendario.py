import datetime
from cal_setup import get_calendar_service

service = get_calendar_service()

d = datetime.now().date()
tomorrow = datetime(d.year, d.month, d.day, 10)+datetime.timedelta(days=1)
start = tomorrow.isoformat()
end = (tomorrow + datetime.timedelta(hours=1)).isoformat()

def addEvent(nombre:str, descripcion:str, inicio:datetime, final: datetime):
    time_zone = 'America/Hermosillo'
    event_result = service.events().insert(calendarId='primary',
       body={
           "summary": nombre,
           "description": descripcion,
           "start": {"dateTime": start, "timeZone": time_zone},
           "end": {"dateTime": end, "timeZone": time_zone},
       }
   ).execute()

def main():
   service = get_calendar_service()
   now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
   events_result = service.events().list(
       calendarId='primary', timeMin=now,
       maxResults=100, singleEvents=True,
       orderBy='startTime').execute()
   events = events_result.get('items', [])

if __name__ == '__main__':
   main()