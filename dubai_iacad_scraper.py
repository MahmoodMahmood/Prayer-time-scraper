from datetime import datetime
import pytz
import requests
from bs4 import BeautifulSoup

class DubaiIacadPrayerTimes:
    def __init__(self):
        self.URL = "https://services.iacad.gov.ae/SmartPortal/Timings"
        self.TIMEZONE_NAME = "GST"
        self.TIMEZONE_TZ = pytz.timezone('Asia/Dubai')
        self.headers = requests.structures.CaseInsensitiveDict()
        self.headers["Cookie"] = "_culture=en-GB"

    def get_athan_times_today(self):
        page = self._get_prayer_time_page()
        return self._get_prayer_times_from_page(page)

    def _time_str_to_time_obj(self, time_str):
        cur_time = datetime.now(self.TIMEZONE_TZ)
        return self.TIMEZONE_TZ.localize(datetime.strptime(f"{cur_time.month}/{cur_time.day}/{cur_time.year} {time_str}", "%m/%d/%Y %I:%M %p"))

    def _get_prayer_time_page(self):
        return requests.get(self.URL, headers=self.headers)

    def _get_prayer_times_from_page(self, page):
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="dt2")

        prayer_names_arr =  [child.text.strip() for child in results.find_all(attrs={"data-title":"Pray name"})]
        prayer_times_str_arr = [child.text.strip() for child in results.find_all(attrs={"data-title":"Time"})]
        prayer_times_arr = [self._time_str_to_time_obj(t) for t in prayer_times_str_arr]
        
        return dict(zip(prayer_names_arr, prayer_times_arr))


if __name__ == "__main__":
    times_getter = DubaiIacadPrayerTimes()
    prayer_times = times_getter.get_athan_times_today()
    fmt = '%Y-%m-%d %I:%M:%S %p %z'
    print([f"{prayer_name}: {prayer_times[prayer_name].strftime(fmt)}" for prayer_name in prayer_times])
