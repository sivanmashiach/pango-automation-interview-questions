from automation_framework.utilities.db_helpers import DatabaseHelper
from automation_framework.utilities.extract_timeanddate import extract_timeanddate_weather
import csv

with open('diff_report.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['City', 'API Temperature', 'TimeAndDate Temperature', 'Difference'])

    timeanddate_data = extract_timeanddate_weather()
    db_helper = DatabaseHelper()
    big_diff_min = 3
    big_diff_count = 0
    for city, timeanddate_temp in timeanddate_data.items():
        db_data = db_helper.get_weather_data(city)
        if not db_data:
            print("city is missing from db", city)
            continue
        db_temp = round(db_data[1])
        temp_diff = abs(db_temp - timeanddate_temp)
        if temp_diff >= big_diff_min:
            big_diff_count += 1
            csv_writer.writerow([city, db_temp, timeanddate_temp, temp_diff])
    print("Big temp diff cities count is", big_diff_count)
