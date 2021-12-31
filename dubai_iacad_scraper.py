import requests
from bs4 import BeautifulSoup

class DubaiIacadPrayerTimes:
    def __init__(self):
        self.URL = "https://services.iacad.gov.ae/SmartPortal/Timings"
        self.headers = requests.structures.CaseInsensitiveDict()
        self.headers["Cookie"] = "_culture=en-GB"

    def get_athan_times_today(self):
        page = self._get_prayer_time_page()
        return self._get_prayer_times_from_page(page)

    def _get_prayer_time_page(self):
        return requests.get(self.URL, headers=self.headers)

    def _get_prayer_times_from_page(self, page):
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="dt2")

        prayer_names_arr =  [child.text.strip() for child in results.find_all(attrs={"data-title":"Pray name"})]
        prayer_times_arr = [child.text.strip() for child in results.find_all(attrs={"data-title":"Time"})]

        return dict(zip(prayer_names_arr, prayer_times_arr))

if __name__ == "__main__":
    times = DubaiIacadPrayerTimes()
    print(times.get_athan_times_today())
