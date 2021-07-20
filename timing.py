import datetime
import time


def get_time_formatted(timestamp):
    timestamp = datetime.datetime.fromtimestamp(timestamp)
    return timestamp.strftime('%H:%M:%S/%d/%m/%y')
    pass


def get_current_timestamp():
    timestamp = time.time()
    return int(timestamp)
    pass


def is_event_time(event_timestamp):
    timestamp_now = get_current_timestamp()
    timestamp_difference = timestamp_now - event_timestamp
    print(
        f"""
    Now:{timestamp_now} = {get_time_formatted(timestamp_now)}
    Event time:{event_timestamp} = {get_time_formatted(event_timestamp)}
    Difference is {timestamp_difference} seconds
    """)
    pass


print(get_current_timestamp())
print(get_time_formatted(get_current_timestamp()))
while True:
    is_event_time(int(input('Enter event timestamp:\n')))
