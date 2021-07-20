def db_record_to_event(db_request_result):
    from rmd_classes import Event

    new_event = Event(
        id=db_request_result[0],
        tg_user_id=db_request_result[1],
        text=db_request_result[2],
        timestamp=db_request_result[3],
        is_forced=False,
        forcing_period=0,
        last_forced=0
    )

    return new_event
