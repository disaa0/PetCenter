from datetime import datetime, timedelta
from cal_setup import get_calendar_service
import googleapiclient

service = get_calendar_service()
def create_event(nombre:str, descripcion:str, inicio:str, final: str)->str:
    time_zone = 'America/Hermosillo'
    event_result = service.events().insert(calendarId='primary',
       body={
           "summary": nombre,
           "description": descripcion,
           "start": {"dateTime": inicio, "timeZone": time_zone},
           "end": {"dateTime": final, "timeZone": time_zone},
       }
   ).execute()

def create_events_dict()->dict:
    dic_eventos = {}
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=3000, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime')
        f = start
        f.replace('T', ' ')
        f =  f[:len(f)-6]
        dt_tuple=tuple([int(x) for x in f[:10].split('-')])+tuple([int(x) for x in f[11:].split(':')])
        fecha_inicio = datetime(*dt_tuple)
        fecha = fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')
        #print(fecha_inicio)
        dic_eventos[fecha] = event['summary']
        print(fecha, event['summary'])
    return dic_eventos

def create_week_list()->list:
    starting_day = datetime.now().date()
    week_list = []
    for number in range(365):
        day = datetime(starting_day.year, starting_day.month, starting_day.day) + timedelta(days=number + 1)
        #print(day)
        week_list.append(day)
    return week_list

def get_available_days_dict()->dict:
    #availible_days = {day:{ hour : True }}
    week_list = create_week_list()
    dic_eventos = create_events_dict()
    availible_days = {}
    for day in week_list:
        for hour in range(8,20):
            fecha = datetime(day.year, day.month, day.day, hour, 0, 0)
            fecha_txt = fecha.strftime('%Y-%m-%d %H:%M:%S')
            llave = day.strftime("%Y-%m-%d")
            hora = fecha.strftime("%H:%M:%S")
        
            if llave not in availible_days:
                availible_days[llave] = {}

            if hora not in availible_days[llave]:
                availible_days[llave][hora] = {}

            if fecha_txt not in dic_eventos.keys():
                availible_days[llave][hora]['disponible'] = True
            else:
                availible_days[llave][hora]['disponible'] = False
            availible_days[llave][hora]['fecha'] = fecha_txt
    return availible_days

def delete_event(event_id:str)->bool:
    try:
        service.events().delete(
            calendarId='primary',
            eventId=event_id,
        ).execute()
        return True
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")
        return False

def search_event(fecha_buscada:str)->str:
    id = ''
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=1000, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime')
        f = start
        f.replace('T', ' ')
        f =  f[:len(f)-6]
        dt_tuple=tuple([int(x) for x in f[:10].split('-')])+tuple([int(x) for x in f[11:].split(':')])
        fecha_inicio = datetime(*dt_tuple)
        fecha = fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')
        #print(fecha_inicio)
        if fecha == fecha_buscada:
            id = event.get('id')
            break
    if id == '':
        print('Event not found.')
    return id

def main():
    # d = datetime.now().date()
    # tomorrow = datetime(d.year, d.month, d.day, 11)+timedelta(days=1)
    # start = tomorrow.isoformat()
    # end = (tomorrow + timedelta(hours=1)).isoformat()
    # #create_event('Cita - Veterinaria. Cliente', 'aasdqwfqwfqfqwfqfqwf', start, end)
    # dic_eventos = create_events_dict()
    # #print(dic_eventos)
    # week_list = create_week_list()
    # available_days = get_available_days_dict(week_list, dic_eventos)
    # for day, hours in available_days.items():
    #     for hour in hours:
    #         disponible = available_days[day][hour]['disponible']
    #         if not disponible:
    #             print(hour)
    id = search_event('2022-05-04 14:00:00')
    print(id)


if __name__ == '__main__':
   main()