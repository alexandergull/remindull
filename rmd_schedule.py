import schedule
import rmd_static
import time
import timing


def check_events(db, polling_period):
    current_timestamp = timing.get_current_timestamp()
    showtime = {'from': current_timestamp - polling_period, 'to': current_timestamp + polling_period}
    print(f"Current time is {timing.get_time_formatted(timing.get_current_timestamp())}")
    print(f"Searching events from {timing.get_time_formatted(showtime['from'])} "
          f"to {timing.get_time_formatted(showtime['to'])}")
    try:
        query = f"""SELECT * FROM events WHERE event_time > {showtime['from']} AND event_time < {showtime['to']}"""
        check_events_result = db.execute_read_query(query)
        for db_event in check_events_result:
            event_object = rmd_static.db_record_to_event(db_event)
            print(event_object.tg_user_id, event_object.text)
    except:
        print('Query error #1')

    # print(check_events_result)


def cron(db, polling_period):
    check_events(db, polling_period)


def init_cron(db, polling_period):
    print(f"Cron with {polling_period} seconds period is polling now..")
    schedule.every(polling_period).seconds.do(cron, db, polling_period)

    while True:
        schedule.run_pending()
        time.sleep(1)
