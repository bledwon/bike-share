-- Cyclistic 2019 analysis (BigQuery-flavored SQL)
-- Assumes raw tables loaded as:
--   my_dataset.trips_2019_q1, trips_2019_q2, trips_2019_q3, trips_2019_q4
-- Q2 columns differ, so we normalize them before UNION.

-- 1) Build a normalized view
CREATE OR REPLACE VIEW my_dataset.trips_2019 AS
WITH q1 AS (
  SELECT
    trip_id,
    start_time,
    end_time,
    bikeid,
    tripduration,
    from_station_id,
    from_station_name,
    to_station_id,
    to_station_name,
    usertype,
    gender,
    birthyear
  FROM my_dataset.trips_2019_q1
),
q2 AS (
  SELECT
    `01 - Rental Details Rental ID` AS trip_id,
    `01 - Rental Details Local Start Time` AS start_time,
    `01 - Rental Details Local End Time` AS end_time,
    `01 - Rental Details Bike ID` AS bikeid,
    `01 - Rental Details Duration In Seconds Uncapped` AS tripduration,
    `03 - Rental Start Station ID` AS from_station_id,
    `03 - Rental Start Station Name` AS from_station_name,
    `02 - Rental End Station ID` AS to_station_id,
    `02 - Rental End Station Name` AS to_station_name,
    `User Type` AS usertype,
    `Member Gender` AS gender,
    `05 - Member Details Member Birthday Year` AS birthyear
  FROM my_dataset.trips_2019_q2
),
q3 AS (
  SELECT
    trip_id,
    start_time,
    end_time,
    bikeid,
    tripduration,
    from_station_id,
    from_station_name,
    to_station_id,
    to_station_name,
    usertype,
    gender,
    birthyear
  FROM my_dataset.trips_2019_q3
),
q4 AS (
  SELECT
    trip_id,
    start_time,
    end_time,
    bikeid,
    tripduration,
    from_station_id,
    from_station_name,
    to_station_id,
    to_station_name,
    usertype,
    gender,
    birthyear
  FROM my_dataset.trips_2019_q4
)
SELECT * FROM q1
UNION ALL SELECT * FROM q2
UNION ALL SELECT * FROM q3
UNION ALL SELECT * FROM q4;

-- 2) Cleaned base table
CREATE OR REPLACE VIEW my_dataset.trips_2019_clean AS
SELECT
  *,
  DATETIME(start_time) AS start_dt,
  DATETIME(end_time) AS end_dt,
  CAST(REPLACE(CAST(tripduration AS STRING), ",", "") AS FLOAT64) AS trip_seconds,
  CASE
    WHEN LOWER(usertype) IN ('subscriber', 'member') THEN 'member'
    WHEN LOWER(usertype) IN ('customer', 'casual') THEN 'casual'
    ELSE 'unknown'
  END AS user_type
FROM my_dataset.trips_2019
WHERE start_time IS NOT NULL
  AND tripduration IS NOT NULL;

-- 3) Summary stats
SELECT
  user_type,
  COUNT(*) AS ride_count,
  AVG(trip_seconds) AS avg_ride_seconds,
  MIN(trip_seconds) AS min_ride_seconds,
  MAX(trip_seconds) AS max_ride_seconds
FROM my_dataset.trips_2019_clean
WHERE trip_seconds > 0
GROUP BY user_type;

-- 4) Rides by day of week (Mon-Sun)
SELECT
  FORMAT_DATETIME('%a', start_dt) AS day_of_week,
  user_type,
  COUNT(*) AS ride_count,
  AVG(trip_seconds) AS avg_ride_seconds
FROM my_dataset.trips_2019_clean
WHERE trip_seconds > 0
GROUP BY day_of_week, user_type
ORDER BY day_of_week, user_type;

-- 5) Rides by hour
SELECT
  EXTRACT(HOUR FROM start_dt) AS hour_of_day,
  user_type,
  COUNT(*) AS ride_count
FROM my_dataset.trips_2019_clean
WHERE trip_seconds > 0
GROUP BY hour_of_day, user_type
ORDER BY hour_of_day, user_type;

-- 6) Rides by month
SELECT
  EXTRACT(MONTH FROM start_dt) AS month,
  user_type,
  COUNT(*) AS ride_count
FROM my_dataset.trips_2019_clean
WHERE trip_seconds > 0
GROUP BY month, user_type
ORDER BY month, user_type;

-- 7) Round-trip share
SELECT
  user_type,
  COUNTIF(from_station_id = to_station_id) AS round_trips,
  COUNT(*) AS total_rides,
  COUNTIF(from_station_id = to_station_id) / COUNT(*) AS round_trip_share
FROM my_dataset.trips_2019_clean
WHERE trip_seconds > 0
GROUP BY user_type;

-- 8) Commute window share (weekday 7-9, 16-18)
SELECT
  user_type,
  COUNTIF(
    EXTRACT(DAYOFWEEK FROM start_dt) BETWEEN 2 AND 6
    AND (EXTRACT(HOUR FROM start_dt) BETWEEN 7 AND 9
         OR EXTRACT(HOUR FROM start_dt) BETWEEN 16 AND 18)
  ) AS commute_rides,
  COUNTIF(EXTRACT(DAYOFWEEK FROM start_dt) BETWEEN 2 AND 6) AS weekday_rides,
  COUNTIF(
    EXTRACT(DAYOFWEEK FROM start_dt) BETWEEN 2 AND 6
    AND (EXTRACT(HOUR FROM start_dt) BETWEEN 7 AND 9
         OR EXTRACT(HOUR FROM start_dt) BETWEEN 16 AND 18)
  ) / COUNTIF(EXTRACT(DAYOFWEEK FROM start_dt) BETWEEN 2 AND 6) AS commute_share
FROM my_dataset.trips_2019_clean
WHERE trip_seconds > 0
GROUP BY user_type;

-- 9) Long ride share (>30 and >60 minutes)
SELECT
  user_type,
  COUNTIF(trip_seconds > 30 * 60) AS rides_over_30m,
  COUNTIF(trip_seconds > 60 * 60) AS rides_over_60m,
  COUNT(*) AS total_rides,
  COUNTIF(trip_seconds > 30 * 60) / COUNT(*) AS share_over_30m,
  COUNTIF(trip_seconds > 60 * 60) / COUNT(*) AS share_over_60m
FROM my_dataset.trips_2019_clean
WHERE trip_seconds > 0
GROUP BY user_type;

-- 10) Top start stations
SELECT
  user_type,
  from_station_name AS station_name,
  COUNT(*) AS ride_count
FROM my_dataset.trips_2019_clean
WHERE trip_seconds > 0
  AND from_station_name IS NOT NULL
GROUP BY user_type, station_name
ORDER BY user_type, ride_count DESC;
