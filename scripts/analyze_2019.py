#!/usr/bin/env python3
"""Analyze 2019 Cyclistic trip data (Q1-Q4 CSVs) with standard library only."""
from __future__ import annotations

import csv
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path

RAW_DIR = Path('/Users/benledwon/Desktop/Github_connection/bike_share/data/raw')
OUT_DIR = Path('/Users/benledwon/Desktop/Github_connection/bike_share/data/processed')

FILES = sorted(RAW_DIR.glob('Trips_2019_Q*.csv'))

# Normalize column names for Q2
Q2_MAP = {
    '01 - Rental Details Rental ID': 'trip_id',
    '01 - Rental Details Local Start Time': 'start_time',
    '01 - Rental Details Local End Time': 'end_time',
    '01 - Rental Details Bike ID': 'bikeid',
    '01 - Rental Details Duration In Seconds Uncapped': 'tripduration',
    '03 - Rental Start Station ID': 'from_station_id',
    '03 - Rental Start Station Name': 'from_station_name',
    '02 - Rental End Station ID': 'to_station_id',
    '02 - Rental End Station Name': 'to_station_name',
    'User Type': 'usertype',
    'Member Gender': 'gender',
    '05 - Member Details Member Birthday Year': 'birthyear',
}

DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def parse_datetime(value: str) -> datetime | None:
    if not value:
        return None
    value = value.strip()
    # Common ISO format: 2019-04-01 00:02:22
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        pass
    # Fallback formats if needed
    for fmt in ('%m/%d/%Y %H:%M', '%m/%d/%Y %H:%M:%S'):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def parse_duration_seconds(value: str) -> int | None:
    if value is None:
        return None
    v = value.strip().replace(',', '')
    if not v:
        return None
    try:
        return int(float(v))
    except ValueError:
        return None


def normalize_row(row: dict) -> dict:
    if 'trip_id' in row:
        return row
    # Q2 mapping
    return {Q2_MAP.get(k, k): v for k, v in row.items()}


def usertype_bucket(usertype: str) -> str:
    if not usertype:
        return 'unknown'
    u = usertype.strip().lower()
    if u in ('subscriber', 'member'):
        return 'member'
    if u in ('customer', 'casual'):
        return 'casual'
    return 'unknown'


def write_csv(path: Path, headers: list[str], rows: list[list]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


# Aggregations
counts_by_user = Counter()
ride_sum_by_user = defaultdict(int)
ride_count_by_user = defaultdict(int)
ride_min_by_user = defaultdict(lambda: None)
ride_max_by_user = defaultdict(lambda: None)

counts_by_day_user = defaultdict(int)  # (day, user) -> count
ride_sum_by_day_user = defaultdict(int)
ride_count_by_day_user = defaultdict(int)

counts_by_hour_user = defaultdict(int)  # (hour, user)
counts_by_month_user = defaultdict(int)  # (month, user)

weekend_counts_by_user = defaultdict(int)
weekday_counts_by_user = defaultdict(int)

commute_counts_by_user = defaultdict(int)  # weekday 7-9 & 16-18

round_trip_counts_by_user = defaultdict(int)

long_ride_30_counts_by_user = defaultdict(int)  # >30 min
long_ride_60_counts_by_user = defaultdict(int)  # >60 min

start_station_counts_member = Counter()
start_station_counts_casual = Counter()

unique_usertypes = Counter()

row_count = 0
bad_time_rows = 0
bad_duration_rows = 0

for file in FILES:
    with file.open('r', newline='') as f:
        reader = csv.DictReader(f)
        for raw_row in reader:
            row_count += 1
            row = normalize_row(raw_row)

            usertype_raw = (row.get('usertype') or '').strip()
            unique_usertypes[usertype_raw] += 1
            user_bucket = usertype_bucket(usertype_raw)

            start_time = parse_datetime(row.get('start_time', ''))
            if start_time is None:
                bad_time_rows += 1
                continue

            duration = parse_duration_seconds(row.get('tripduration', ''))
            if duration is None or duration < 0:
                bad_duration_rows += 1
                continue

            # Core counts
            counts_by_user[user_bucket] += 1
            ride_sum_by_user[user_bucket] += duration
            ride_count_by_user[user_bucket] += 1

            prev_min = ride_min_by_user[user_bucket]
            prev_max = ride_max_by_user[user_bucket]
            ride_min_by_user[user_bucket] = duration if prev_min is None else min(prev_min, duration)
            ride_max_by_user[user_bucket] = duration if prev_max is None else max(prev_max, duration)

            # Day of week
            day = DAY_NAMES[start_time.weekday()]  # Mon..Sun
            counts_by_day_user[(day, user_bucket)] += 1
            ride_sum_by_day_user[(day, user_bucket)] += duration
            ride_count_by_day_user[(day, user_bucket)] += 1

            # Hour
            counts_by_hour_user[(start_time.hour, user_bucket)] += 1

            # Month
            counts_by_month_user[(start_time.month, user_bucket)] += 1

            # Weekend vs weekday
            if start_time.weekday() >= 5:
                weekend_counts_by_user[user_bucket] += 1
            else:
                weekday_counts_by_user[user_bucket] += 1

            # Commute windows (weekday 7-9 and 16-18)
            if start_time.weekday() < 5 and (7 <= start_time.hour <= 9 or 16 <= start_time.hour <= 18):
                commute_counts_by_user[user_bucket] += 1

            # Round trips (same start/end)
            if (row.get('from_station_id') or '').strip() and (row.get('to_station_id') or '').strip():
                if row.get('from_station_id') == row.get('to_station_id'):
                    round_trip_counts_by_user[user_bucket] += 1

            # Long ride shares
            if duration > 30 * 60:
                long_ride_30_counts_by_user[user_bucket] += 1
            if duration > 60 * 60:
                long_ride_60_counts_by_user[user_bucket] += 1

            # Start station counts
            start_station = (row.get('from_station_name') or '').strip()
            if start_station:
                if user_bucket == 'member':
                    start_station_counts_member[start_station] += 1
                elif user_bucket == 'casual':
                    start_station_counts_casual[start_station] += 1


# Build outputs
# Overall summary
summary_rows = []
for user in ['member', 'casual', 'unknown']:
    cnt = counts_by_user[user]
    if cnt == 0:
        avg = 0
    else:
        avg = ride_sum_by_user[user] / cnt
    summary_rows.append([
        user,
        cnt,
        round(avg, 2),
        ride_min_by_user[user] or '',
        ride_max_by_user[user] or '',
        weekend_counts_by_user[user],
        weekday_counts_by_user[user],
    ])

write_csv(
    OUT_DIR / 'summary_overall.csv',
    ['user_type', 'ride_count', 'avg_ride_seconds', 'min_ride_seconds', 'max_ride_seconds', 'weekend_rides', 'weekday_rides'],
    summary_rows,
)

# Counts by day
rows = []
for day in DAY_NAMES:
    for user in ['member', 'casual', 'unknown']:
        rows.append([day, user, counts_by_day_user[(day, user)]])
write_csv(
    OUT_DIR / 'rides_by_day_user.csv',
    ['day_of_week', 'user_type', 'ride_count'],
    rows,
)

# Avg ride length by day
rows = []
for day in DAY_NAMES:
    for user in ['member', 'casual', 'unknown']:
        cnt = ride_count_by_day_user[(day, user)]
        avg = (ride_sum_by_day_user[(day, user)] / cnt) if cnt else 0
        rows.append([day, user, round(avg, 2)])
write_csv(
    OUT_DIR / 'avg_ride_seconds_by_day_user.csv',
    ['day_of_week', 'user_type', 'avg_ride_seconds'],
    rows,
)

# Counts by hour
rows = []
for hour in range(24):
    for user in ['member', 'casual', 'unknown']:
        rows.append([hour, user, counts_by_hour_user[(hour, user)]])
write_csv(
    OUT_DIR / 'rides_by_hour_user.csv',
    ['hour_of_day', 'user_type', 'ride_count'],
    rows,
)

# Counts by month
rows = []
for month in range(1, 13):
    for user in ['member', 'casual', 'unknown']:
        rows.append([month, user, counts_by_month_user[(month, user)]])
write_csv(
    OUT_DIR / 'rides_by_month_user.csv',
    ['month', 'user_type', 'ride_count'],
    rows,
)

# Commute share
rows = []
for user in ['member', 'casual', 'unknown']:
    total_weekday = weekday_counts_by_user[user]
    commute = commute_counts_by_user[user]
    share = (commute / total_weekday) if total_weekday else 0
    rows.append([user, commute, total_weekday, round(share, 4)])
write_csv(
    OUT_DIR / 'commute_share_weekday.csv',
    ['user_type', 'commute_rides', 'weekday_rides', 'commute_share'],
    rows,
)

# Round trip share
rows = []
for user in ['member', 'casual', 'unknown']:
    total = counts_by_user[user]
    round_trips = round_trip_counts_by_user[user]
    share = (round_trips / total) if total else 0
    rows.append([user, round_trips, total, round(share, 4)])
write_csv(
    OUT_DIR / 'round_trip_share.csv',
    ['user_type', 'round_trip_rides', 'total_rides', 'round_trip_share'],
    rows,
)

# Long ride share
rows = []
for user in ['member', 'casual', 'unknown']:
    total = counts_by_user[user]
    over_30 = long_ride_30_counts_by_user[user]
    over_60 = long_ride_60_counts_by_user[user]
    rows.append([
        user,
        over_30,
        over_60,
        total,
        round((over_30 / total) if total else 0, 4),
        round((over_60 / total) if total else 0, 4),
    ])
write_csv(
    OUT_DIR / 'long_ride_share.csv',
    ['user_type', 'rides_over_30m', 'rides_over_60m', 'total_rides', 'share_over_30m', 'share_over_60m'],
    rows,
)

# Top start stations
write_csv(
    OUT_DIR / 'top_start_stations_member.csv',
    ['station_name', 'ride_count'],
    start_station_counts_member.most_common(20),
)
write_csv(
    OUT_DIR / 'top_start_stations_casual.csv',
    ['station_name', 'ride_count'],
    start_station_counts_casual.most_common(20),
)

# Metadata
write_csv(
    OUT_DIR / 'analysis_metadata.csv',
    ['metric', 'value'],
    [
        ['rows_processed', row_count],
        ['bad_time_rows', bad_time_rows],
        ['bad_duration_rows', bad_duration_rows],
    ] + [[f'usertype_raw:{k}', v] for k, v in unique_usertypes.most_common()],
)

print('Done.')
