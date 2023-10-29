from datetime import datetime, timedelta
from gcsa.google_calendar import GoogleCalendar


def get_calendar_events(sentence):
    dates = extract_dates(sentence)
    start = dates["start"]
    end = dates["end"]

    gc = GoogleCalendar(credentials_path=".credentials/credentials.json")
    events = []
    for event in gc.get_events(start, end, order_by='startTime', single_events=True):
        events.append(f"- {event.summary} at {event.location} from {event.start.strftime('%I:%M%p')} to {event.end.strftime('%I:%M%p')}")

    if events:
        return f"{len(events)} events from {start.strftime('%d %B %Y')} to {end.strftime('%d %B %Y')} in Fox's calendar:\n" + '\n'.join(events)
    else:
        return None


def extract_dates(sentence):
    if "yesterday" in sentence or "the other day" in sentence or "yest" in sentence:
        print("User asked for calendar info from yesterday.")
        start_date = datetime.today() + timedelta(days=-1)
        end_date = datetime.today()
    elif "tomorrow" in sentence or "tmrw" in sentence or "tmr" in sentence:
        print("User asked for calendar info for tomorrow.")
        start_date = datetime.today() + timedelta(days=1)
        end_date = datetime.today() + timedelta(days=2)
    elif "week" in sentence or "future" in sentence:
        print("User asked for calendar info for the upcoming week.")
        start_date = datetime.today()
        end_date = datetime.today() + timedelta(days=8)
    else:
        print("User asked for calendar info for today.")
        start_date = datetime.today()
        end_date = datetime.today() + timedelta(days=1)
    return {
        "start": start_date,
        "end": end_date,
    }


if __name__ == '__main__':
    print(get_calendar_events("What do I have this week?"))
