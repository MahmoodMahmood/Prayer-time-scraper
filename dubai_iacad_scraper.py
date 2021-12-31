import requests
from bs4 import BeautifulSoup

def get_prayer_time_page():
    URL = "https://services.iacad.gov.ae/SmartPortal/Timings"
    headers = requests.structures.CaseInsensitiveDict()
    headers["Cookie"] = "_culture=en-GB"
    return requests.get(URL, headers=headers)

def get_prayer_times_from_page(page):
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="dt2")

    prayer_names_arr =  [child.text.strip() for child in results.find_all(attrs={"data-title":"Pray name"})]
    prayer_times_arr = [child.text.strip() for child in results.find_all(attrs={"data-title":"Time"})]

    return dict(zip(prayer_names_arr, prayer_times_arr))

page = get_prayer_time_page()
print(get_prayer_times_from_page(page))