<h1>Store Monitoring System</h1>

This repository contains the backend system for monitoring the status of restaurants in the US. The system tracks the online/offline status of these restaurants during their business hours and provides detailed reports on store uptime and downtime.
Problem

The goal of this project is to monitor the operational status of multiple restaurants. Each restaurant is expected to be online during its designated business hours. However, due to various reasons, a restaurant might go offline temporarily. Restaurant owners require a historical report of such occurrences.
Data Source

The data source for this system is a CSV file located in /store/main/csv_data. The CSV file contains the following columns:

    store_id: Unique identifier for each restaurant.
    timestamp_utc: Timestamp in UTC indicating when the status was recorded.
    status: Indicates whether the store is active or inactive.

Additional data sources include:

    Business hours data, which includes the restaurant's opening and closing times for each day of the week.
    Timezone information for each restaurant.

APIs

The system provides the following APIs to generate reports:
Trigger Report

This API triggers the generation of a report for a specific restaurant.

Endpoint: GET /store/{store_id}/trigger_report/

Request:

shell

curl --request GET \
  --url http://localhost:8000/store/{store_id}/trigger_report/ \
  --header 'Content-Type: application/json' \
  --data ' '

Get Report

This API retrieves the status report for a restaurant based on a provided report_id.

Endpoint: POST /store/get_report/

Request:

shell

curl --request POST \
  --url http://localhost:8000/store/get_report/ \
  --header 'Content-Type: application/json' \
  --data '{
    "report_id": 74
  }'

Solution

The system is built using the Python Django framework and utilizes a PostgreSQL database. The logic for calculating uptime and downtime for the last one day, one hour, and one week is as follows:

    Initialize a dictionary called last_one_day_data with keys "uptime," "downtime," and "unit." Set "uptime" and "downtime" to 0 and "unit" to "hours."

    Calculate one_day_ago as the day of the week one day before the current day. If the current day is 0 (Monday), set one_day_ago to 6 (Sunday).

    Check if the restaurant was open during the last one day (from one_day_ago to current_day) at the current time (current_time). This is determined by querying the restaurant's business hours.

    If the restaurant was not open during the last one day, return the initialized last_one_day_data.

    If the restaurant was open during the last one day, query the status logs for all logs within the last one day (from utc_time - 1 day to utc_time) and order them by timestamp.

    Loop through each log in last_one_day_logs:
        Check if the log's timestamp falls within the restaurant's business hours on that day (log_in_store_business_hours).
        If the log is not within the restaurant's business hours, skip it and move to the next log.
        If the log's status is "active," increment the "uptime" value in last_one_day_data by 1 hour.
        If the log's status is not "active," increment the "downtime" value in last_one_day_data by 1 hour.

The same logic is applied to calculate uptime and downtime for the last one hour and last one week.

This system aims to provide restaurant owners with valuable insights into their stores' operational status, helping them make informed decisions to improve uptime and customer experience.