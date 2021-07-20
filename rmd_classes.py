class Event:
    def __init__(self,
                 id=0,
                 tg_user_id="",
                 text="",
                 timestamp=0,
                 is_forced=False,
                 forcing_period=0,
                 last_forced=0
                 ):
        self.id = id
        self.tg_user_id = tg_user_id
        self.text = text
        self.timestamp = timestamp
        self.is_forced = is_forced
        self.forcing_period = forcing_period
        self.last_forced = last_forced
