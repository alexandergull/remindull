import rmd_sqlite
import datetime
import time
import rmd_schedule
import rmd_static


def add_event(db):
    user_id = input('Enter user_id\n')
    event_text = input('Enter event text\n')
    input_time = input('Enter event time in format of 00:00/dd/mm/yy\n')

    event_timestamp = time.mktime(datetime.datetime.strptime(input_time, "%H:%M/%d/%m/%y").timetuple())

    db.query_set_new_event(user_id, event_text, event_timestamp)
    pass


def get_datetime_from_timestamp(timestamp):
    tstp = datetime.datetime.fromtimestamp(timestamp)
    return tstp.strftime('%H:%M/%d/%m/%y')


def show_events(db):
    user_id = input('Enter user id:\n')
    events_list = db.query_get_user_events(user_id)
    print(f'List of events of user_id={user_id}')
    for key in events_list:
        event = rmd_static.db_record_to_event(key)
        print(f'Event ID: {event.key_id}')
        print(f'Event text: {event.text}')
        print(f'Event tg_user_id: {event.tg_user_id}')
        print(f'Event timestamp: {event.timestamp}')
        print(f'Event is forced: {event.is_forced}')
        print(f'Event forcing period: {event.forcing_period}')
        print(f'Event last forced time: {event.last_forced}')
        print(f'Event initial time: {event.initial_timestamp}')
        print(f'Event forcing count: {event.forcing_count}\n')
    pass


def add_user(db):
    tg_user_id = input('Enter new user tg_id:\n')
    user_name = input('Enter new user name:\n')
    forcing_period = input('Enter forcing period (minutes)\n')
    timezone = input('Enter timezone (5 or -5)\n')
    data = [None, tg_user_id, forcing_period, timezone, user_name]
    db.query_set_new_user(data)


def show_user_data(db, tg_user_id):
    current_state = db.execute_read_query(f"SELECT * FROM users WHERE tg_user_id = '{tg_user_id}'")
    print(f'USER TG_ID: {current_state[0][1]}')
    print(f'USER NAME: {current_state[0][4]}')
    print(f'USER FORCING PERIOD: {current_state[0][2]}')
    print(f'USER TIMEZONE: {current_state[0][3]}')


def show_user_data_by_id(db):
    tg_user_id = input('Enter tg_user_id:\n')
    show_user_data(db, tg_user_id)


def show_all_users_data(db):
    users_list = db.execute_read_query(f"SELECT tg_user_id FROM users")
    for user in users_list:
        show_user_data(db, user[0])
        print('\n')


def edit_user(db):
    tg_user_id = input('Enter user tg_id that needs to update, enter -- to skip changes:\n')
    show_user_data(db, tg_user_id)
    current_state = db.execute_read_query(f"SELECT * FROM users WHERE tg_user_id = '{tg_user_id}'")
    user_name = input('Enter new user name, enter -- to skip changes:\n')
    if user_name == '--':
        user_name = current_state[0][4]
        print(f'Username is kept as it is ({user_name})')
    forcing_period = input('Enter forcing period (minutes), enter -- to skip changes\n')
    if forcing_period == '--':
        forcing_period = current_state[0][2]
        print(f'Forcing period is kept as it is ({forcing_period})')
    timezone = input('Enter timezone (5 or -5), enter -- to skip changes\n')
    if timezone == '--':
        timezone = current_state[0][3]
        print(f'Timezone is kept as it is ({timezone})')
    db.query_update_user(tg_user_id, forcing_period, timezone, user_name)
    show_user_data(db, tg_user_id)


def start_polling(db):
    polling_period = input('Enter polling period')
    rmd_schedule.init_cron(db, int(polling_period))
    pass


def mode_select(db):
    case = int(input("""Select mode:
    1: Add event
    2: Show user events
    3: Add user
    4: Edit user
    5: Show all users
    6: Show user by tg_user_id
    7: Start polling
    0:exit\n"""))
    if case == 1:
        add_event(db)
        mode_select(db)
    elif case == 2:
        show_events(db)
        mode_select(db)
    elif case == 3:
        add_user(db)
        mode_select(db)
    elif case == 4:
        edit_user(db)
        mode_select(db)
    elif case == 5:
        show_all_users_data(db)
        mode_select(db)
    elif case == 6:
        show_user_data_by_id(db)
        mode_select(db)
    elif case == 7:
        start_polling(db)
        mode_select(db)
    elif case == 0:
        exit(0)
    else:
        print('Error in mode_select')
        mode_select(db)


rmd_db = rmd_sqlite.RmdDb('remindull.sqlite')

mode_select(rmd_db)
