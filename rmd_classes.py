class Event:
    def __init__(self,
                 key_id=0,
                 tg_user_id="",
                 text="",
                 timestamp=0,
                 is_forced=False,
                 forcing_period=0,
                 last_forced=0,
                 initial_timestamp=0,
                 forcing_count=0
                 ):
        self.key_id = key_id
        self.tg_user_id = tg_user_id
        self.text = text
        self.timestamp = timestamp
        self.is_forced = is_forced
        self.forcing_period = forcing_period
        self.last_forced = last_forced
        self.initial_timestamp = initial_timestamp
        self.forcing_count = forcing_count

    def force_event(self, custom_forcing_period):
        self.is_forced = True
        if custom_forcing_period:
            self.timestamp += custom_forcing_period
        else:
            self.timestamp += self.forcing_period
        self.forcing_count += 1
