from scraper import Scraper
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import pytz
import requests

class DubaiIacadPrayerTimes(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.URL = "https://services.iacad.gov.ae/SmartPortal/PrayerTimings/Timings/DailyPrayingTimeOfCity?cityId=1&countryId=1&hijriOrGreg=1"
        self.TIMEZONE_TZ = pytz.timezone('Asia/Dubai')
        self.headers = requests.structures.CaseInsensitiveDict()
        self.headers["Cookie"] = "_culture=en-GB"

    def get_athan_times(self, date=datetime.now()):
        page = self._get_prayer_time_page(date)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="dt2")

        prayer_names_arr = [child.text.strip() for child in results.find_all(
            attrs={"data-title": "Pray name"})]
        prayer_times_str_arr = [
            child.text.strip() for child in results.find_all(attrs={"data-title": "Time"})]
        prayer_times_arr = [self._time_str_to_time_obj(t, date) for t in prayer_times_str_arr]

        return dict(zip(prayer_names_arr, prayer_times_arr))

    def _get_prayer_time_page(self, date):
        date_local = self.TIMEZONE_TZ.localize(date)
        date_str = f"&date={date_local.year}/{date_local.month}/{date_local.day}"
        return requests.get(self.URL+date_str, headers=self.headers)

if __name__ == "__main__":
    scraper = DubaiIacadPrayerTimes()
    prayer_times = scraper.get_athan_times()
    print([f"{prayer_name}: {prayer_times[prayer_name].strftime(scraper.get_fmt())}" \
         for prayer_name in prayer_times])
    print(f"nearest prayer is: {scraper.prayer_tuple_to_str(scraper.get_nearest_prayer())}")
    print(f"next prayer is: {scraper.prayer_tuple_to_str(scraper.get_next_prayer())}")