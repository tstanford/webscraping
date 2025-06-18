import requests
import json
from bs4 import BeautifulSoup

url = "https://www.fife.gov.uk/kb/docs/articles/education2/schools-in-fife/school-holidays,-term,-and-closure-dates"

def getEventType(description):
    if description == 'School in-service day':
        return description

    return description.split(" - ")[1]

def main():
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    content = soup.find_all("div", class_="atcb")

    for item in content:
        calendarEntry = json.loads(item.text.strip())
        
        description = calendarEntry["name"]
        startDate = calendarEntry["startDate"].split(" ")[0]
        endDate = calendarEntry["endDate"].split(" ")[0]
        eventType = getEventType(description)

        if eventType != "School term": 
            print("{}, {}, {}".format(description, startDate, endDate))

if __name__ == '__main__':
    main()
