def db_record_to_event(db_request_result):
    from rmd_classes import Event

    new_event = Event(
        key_id=db_request_result[0],
        tg_user_id=db_request_result[1],
        text=db_request_result[2],
        timestamp=db_request_result[3],
        is_forced=db_request_result[4],
        forcing_period=db_request_result[5],
        last_forced=db_request_result[6],
        initial_timestamp=db_request_result[7],
        forcing_count=db_request_result[8]
    )

    return new_event
