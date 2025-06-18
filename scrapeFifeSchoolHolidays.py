import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

url = "https://www.fife.gov.uk/kb/docs/articles/education2/schools-in-fife/school-holidays,-term,-and-closure-dates"

def getEventType(description):
    if description == 'School in-service day':
        return description

    return description.split(" - ")[1]

def getCsv(holidays):
    csv = ""
    for holiday in holidays:
        csv += "%s, %s, %s\n" % holiday
    return csv

def getVcal(holidays):
    cal = ""
    cal += "BEGIN:VCALENDAR\n"
    cal += "PRODID:-//Microsoft Corporation//Outlook 16.0 MIMEDIR//EN\n"
    cal += "VERSION:2.0\n"

    for holiday in holidays:
        startDate = datetime.strptime(holiday[1], "%Y-%m-%d").date()
        endDate = datetime.strptime(holiday[2], "%Y-%m-%d").date() + timedelta(days=1)

        event = ""
        event += "BEGIN:VEVENT\n"
        event += "SUMMARY: "+holiday[0]+"\n"
        event += "DTSTART;VALUE=DATE:"+startDate.strftime("%Y%m%d")+"\n"
        event += "DTEND;VALUE=DATE:"+endDate.strftime("%Y%m%d")+"\n"
        event += "UID:"+startDate.strftime("%Y%m%d")+"_SchoolHol_0000000000".ljust(36,"0")+"\n"
        event += "END:VEVENT\n";
        cal += event

    cal += "END:VCALENDAR\n";

    return cal

def main():
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    content = soup.find_all("div", class_="atcb")
    holidays = []

    for item in content:
        calendarEntry = json.loads(item.text.strip())
        
        description = calendarEntry["name"]
        startDate = calendarEntry["startDate"].split(" ")[0]
        endDate = calendarEntry["endDate"].split(" ")[0]
        eventType = getEventType(description)       

        if eventType != "School term": 
            holiday = (description, startDate, endDate)
            holidays.append(holiday)

    csv = getCsv(holidays)
    vcal = getVcal(holidays)

    print(vcal)

if __name__ == '__main__':
    main()
