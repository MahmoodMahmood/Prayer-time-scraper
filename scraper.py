from datetime import datetime, timedelta

class Scraper:
    def __init__(self):
        self.fmt = '%Y-%m-%d %I:%M:%S %p %z'

    def get_next_prayer(self, max_retries=2):
        cur_time = datetime.now()
        next_prayer = None
        retries = 0
        while next_prayer is None and retries < max_retries:
            prayers = self.get_athan_times(cur_time)
            next_prayer = self._get_next_prayer_from_dict(prayers)
            cur_time += timedelta(days=1)
            retries+=1
        return next_prayer

    def prayer_tuple_to_str(self, prayer_tuple):
        if prayer_tuple is None:
            return ""
        return f"{prayer_tuple[0]}: {prayer_tuple[1].strftime(self.fmt)}"

    def get_nearest_prayer(self):
        prayers_today = self.get_athan_times()
        cur_time = datetime.now(self.TIMEZONE_TZ)
        nearest_prayer_name = min(prayers_today, key=lambda prayer_name: abs(
            cur_time - prayers_today[prayer_name]))
        return (nearest_prayer_name, prayers_today[nearest_prayer_name])

    def get_tz(self):
        return self.TIMEZONE_TZ

    def get_fmt(self):
        return self.fmt

    def get_athan_times(self, date=datetime.now()):
        raise NotImplementedError("Please Implement this method")

    def _get_next_prayer_from_dict(self, prayers):
        cur_time = datetime.now(self.TIMEZONE_TZ)
        next_prayer_name = min(prayers, key=lambda prayer_name: 
            prayers[prayer_name] - cur_time if cur_time < prayers[prayer_name] else timedelta.max)
        if cur_time < prayers[next_prayer_name]:
            return next_prayer_name, prayers[next_prayer_name]
        else:
            return None

    def _time_str_to_time_obj(self, time_str, date=datetime.now()):
        return self.TIMEZONE_TZ.localize(datetime.strptime(
            f"{date.month}/{date.day}/{date.year} {time_str}", "%m/%d/%Y %I:%M %p"))

    def _get_prayer_time_page(self, date):
        raise NotImplementedError("Please Implement this method")