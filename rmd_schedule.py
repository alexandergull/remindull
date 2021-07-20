import schedule
import rmd_static

import time


def check_events(db):
    query = """SELECT * FROM events"""
    check_events_result = db.execute_read_query(query)
    for db_event in check_events_result:
        rmd_static.db_record_to_event(db_event)

    # print(check_events_result)


def cron(db):
    check_events(db)


def init_cron(db, seconds):
    print(f"Cron with {seconds} seconds period is polling now..")
    schedule.every(seconds).seconds.do(cron, db)

    while True:
        schedule.run_pending()
        time.sleep(1)

